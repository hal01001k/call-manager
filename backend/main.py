from fastapi import FastAPI


app = FastAPI(title="Call Manager API")


@app.get("/")
def root():
    return {"message": "Call Manager API is running"}
