from datetime import datetime
from typing import List

from fastapi import FastAPI, Request
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse

templates = Jinja2Templates(directory="templates")

app = FastAPI()


class Record(BaseModel):
    date: str = None
    subject: str
    body: str


data = list()


@app.get("/list", response_model=List[Record])
async def get_all(request: Request):
    return templates.TemplateResponse("list.html", {"request": request, "articles": data})


@app.post("/", response_model=Record)
async def create_new(request: Request):
    incoming_data = await request.form()
    new_data = Record(**incoming_data)
    date = datetime.now()
    new_data.date = date.isoformat()
    data.append(new_data)
    return templates.TemplateResponse("list.html", {"request": request, "articles": data})


@app.get("/")
async def index():
    content = """
    <html>
        <body>
            {body}
        </body>
    </html>
    """.format(body=open("templates/index.html").read())
    return HTMLResponse(content=content)
