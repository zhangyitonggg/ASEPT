from typing import Union
from pathlib import Path
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import backend.convert as convert
import shutil

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.post("/api/problem_file_upload/")
def problem_file_upload(file: UploadFile = File(...)):
    file_path = UPLOAD_DIRECTORY / convert.md5_filename(file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    res = convert.convert2text(file_path)
    if res == None:
        return {"error": "Only PDF and IMAGE files are allowed."}
    else:
        return {"text": res}



@app.get("/api/", response_class=HTMLResponse)
async def welcome():
    return """
    <html>
        <body>
            <h1>Welcome to shared exercise platform!</h1>
        </body>
        <body>
            This is api page. Response is in HTML format.
        </body>
    </html>
    """


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/print/{info}")
async def print_(info: str):
    print(info)
    return {"info": info}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)