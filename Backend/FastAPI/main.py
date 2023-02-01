from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Hola Drixner!"


@app.get("/url")
async def url():
    return {"url":"https://drixner.github.io/myportfolio/"}
