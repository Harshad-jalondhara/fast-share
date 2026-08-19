from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.database import Base, SessionLocal, engine
import app.models
import asyncio
from contextlib import asynccontextmanager

from app.routers import upload, share
from app.services.cleanup_service import cleanup_expired_uploads

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fast Share API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(upload.router)
app.include_router(share.router)



@app.get("/")
def home():
    return {"Fast Share Backend Running"}

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "success", "message": "Database connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed : {str(e)}")

async def cleanup_loop():

    while True:

        db = SessionLocal()

        try:
            deleted_count = cleanup_expired_uploads(db)

            if deleted_count > 0:
                print(
                    f"Cleanup: {deleted_count} expired upload(s) deleted"
                )

        except Exception as error:
            print(f"Cleanup error: {error}")

        finally:
            db.close()

        await asyncio.sleep(5 * 60)

@asynccontextmanager
async def lifespan(app: FastAPI):

    cleanup_task = asyncio.create_task(cleanup_loop())

    yield

    cleanup_task.cancel()

    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass
