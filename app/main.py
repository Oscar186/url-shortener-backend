from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.storage import url_db
from app.utils import generate_short_code

app = FastAPI()

@app.get("/healthcheck")
def health():
    return {"status": "OK"}

@app.post("/shorten")
def shorten_url(original_url: str):
    short_code = generate_short_code()
    url_db[short_code] = original_url

    return {
        "short_url": f"http://127.0.0.1:8000/{short_code}"
    }


#Redirect EndPoint
@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    if short_code not in url_db:
        raise HTTPException(status_code = 404, detail = "URL not found")

    return RedirectResponse(url = url_db[short_code],status_code = 302)