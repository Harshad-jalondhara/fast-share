from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.database import engine, Base

import app.models

from app.routers import upload, share

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fast Share API")



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
