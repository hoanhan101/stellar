from datetime import datetime, timedelta

import redis
from fastapi import FastAPI, HTTPException
from starlette.requests import Request

app = FastAPI()
cache = redis.Redis(host="redis", port=6379)


@app.get("/status")
async def status():
    payload = {"server": "healthy", "redis": "unhealhty"}
    if cache.ping():
        payload["redis"] = "healthy"

    return payload


@app.post("/snippets")
async def create_snippets(request: Request, payload: dict):
    k = payload["name"]
    t = payload["expires_in"]
    v = payload["snippet"]

    now = datetime.now()
    future = now + timedelta(seconds=t)
    future_str = future.strftime("%Y-%m-%dT%H:%M:%SZ")

    cache.setex(k, t, v)
    cache.setex(f"{k}_ttl", t, future_str)

    return {
        "url": f"{request.url._url}/{k}",
        "name": k,
        "expires_at": future_str,
        "ttl": cache.ttl(k),
        "snippet": v,
    }


@app.get("/snippets/{k}")
async def get_snippet(request: Request, k: str):
    v = cache.get(k)
    if v is None:
        raise HTTPException(status_code=404)

    return {
        "url": f"{request.url._url}",
        "name": k,
        "expires_at": cache.get(f"{k}_ttl"),
        "ttl": cache.ttl(k),
        "snippet": v,
    }


@app.get("/snippets/{k}/like")
async def like_snippet(request: Request, k: str):
    v = cache.get(k)
    if v is None:
        raise HTTPException(status_code=404)

    delta = 30
    ttl = cache.ttl(k) + delta
    future_str = cache.get(f"{k}_ttl")
    if future_str is None:
        raise HTTPException(status_code=404)

    future = datetime.strptime(future_str.decode("utf-8"), "%Y-%m-%dT%H:%M:%SZ")
    future_next = future + timedelta(seconds=delta)
    future_next_str = future_next.strftime("%Y-%m-%dT%H:%M:%SZ")

    cache.setex(k, ttl, v)
    cache.setex(f"{k}_ttl", ttl, future_next_str)

    return {
        "url": f"{request.url._url}",
        "name": k,
        "expires_at": future_next_str,
        "ttl": ttl,
        "snippet": v,
    }
