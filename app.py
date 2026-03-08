from fastapi import FastAPI ,Form ,Body,Request, Response, File,Depends,HTTPException,status
from fastapi.responses import  RedirectResponse, JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import uvicorn 
import os
import aiofiles
import json
import csv

from src.helper import file_processing

# from src.helper import llm_pipeline

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")

template = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request : Request):
    return template.TemplateResponse("index.html",{"request" : request})


@app.post("/upload")
async def chat(request : Request , pdf_file : bytes = File(), filename : str = Form(...)):
    base_folder = 'static/docs'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    pdf_filename = os.path.join(base_folder, filename)

    async with aiofiles.open(pdf_filename,'wb') as f:
        await f.write(pdf_file)

    response_data = jsonable_encoder(json.dumps({"msg" : "success" , "pdf_filename" : pdf_filename}))
    res = Response(response_data)
    return res


@app.post("/summarize")
async def summarize_pdf(pdf_filename: str = Body(...)):
    res = file_processing(pdf_filename)
    # print(pdf_filename)  # string
    return res



if __name__ == "__main__":
    uvicorn.run("app:app",host='0.0.0.0',port=8080,reload=True)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React origin
    allow_methods=["*"],
    allow_headers=["*"],
)


