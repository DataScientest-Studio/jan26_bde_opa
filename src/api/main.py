from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API fonctionne"}

@app.get("/stats")
def stats():
    return {"test": "ok"}