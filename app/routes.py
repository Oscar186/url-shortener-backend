import string
import random
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.models import URLRequest
from app.storage import url_db

router = APIRouter()

def generate_short_code(length = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@router.post('/shorten')
def shorten_url(request: URLRequest):
    short_code = generate_short_code()
    url_db[short_code] = str(request.long_url)

    return {
        "short_url": f"http://127.0.0.1:8000/{short_code}"
    }

@router.get("/short_code")
def redirect_url(short_code: str):
    if short_code not in url_db:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url_db[short_code])