from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

items = []

@app.get("/sets")
async def get_items():
    return JSONResponse(content=items)

@app.post("/sets")
async def add_item(request: Request):
    item = await request.json()
    items.append(item)
    return JSONResponse(content=item, status_code=201)
