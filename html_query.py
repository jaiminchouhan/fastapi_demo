from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()


@app.get("/hello/")
def hello():
    ret = ''' 
    <html>
        <body>
            <h1> hello world </h1>
        </body>
    </html>
    '''
    return HTMLResponse(content=ret)


templates = Jinja2Templates(directory="templates")


@app.get("/hellofromtemplate/", response_class=HTMLResponse)
def hello_from_template(request: Request):
    return templates.TemplateResponse("hellohtmltemplate.html", {"request":request})