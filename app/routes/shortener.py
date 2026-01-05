import string, random
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import URL
from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    long_url: HttpUrl

router = APIRouter()

def generate_short_code(length=6):
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )

@router.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):

    long_url = request.long_url
    # Deduplication
    existing = db.query(URL).filter(URL.long_url == long_url).first()
    if existing:
        return {
            "short_url": f"http://127.0.0.1:8000/api/{existing.short_code}"
        }

    # Generate unique short code
    while True:
        short_code = generate_short_code()
        if not db.query(URL).filter(URL.short_code == short_code).first():
            break

    url = URL(
        long_url=long_url,
        short_code=short_code,
        clicks=0
    )

    db.add(url)
    db.commit()      # ✅ IMPORTANT
    db.refresh(url)

    return {
        "short_url": f"http://127.0.0.1:8000/api/{short_code}"
    }

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.clicks = (url.clicks or 0) + 1
    db.commit()

    return RedirectResponse(
        url = url.long_url,
        status_code = 302
    )

@router.get("/stats/{short_code}")
def url_stats(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
        "long_url": url.long_url,
        "short_code": url.short_code,
        "clicks": url.clicks,
        "created_at": url.created_at
    }

# import string
# import random
# from fastapi import APIRouter, HTTPException
# from fastapi.responses import RedirectResponse

# from app.models import URLRequest
# from app.storage import url_db

# router = APIRouter()

# def generate_short_code(length = 6):
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for _ in range(length))

# @router.post('/shorten')
# def shorten_url(request: URLRequest):
#     short_code = generate_short_code()
#     url_db[short_code] = str(request.long_url)

#     return {
#         "short_url": f"http://127.0.0.1:8000/{short_code}"
#     }

# @router.get("/short_code")
# def redirect_url(short_code: str):
#     if short_code not in url_db:
#         raise HTTPException(status_code=404, detail="URL not found")
#     return RedirectResponse(url_db[short_code])