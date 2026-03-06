import json
import os
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xcztsdhhmhopwluyflwj.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_X2Vv6U4GiQw9rqY_0IR--w_Lycky-_k")

DATE_FIELDS = {"borrowed_time", "return_time"}


def _require_config():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Set SUPABASE_URL and SUPABASE_KEY before running the app.")


def _headers(prefer=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    return headers


def _request(method, path, query="", payload=None, headers=None):
    _require_config()
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    if query:
        url = f"{url}?{query}"

    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=body, method=method)

    for key, value in (headers or _headers()).items():
        request.add_header(key, value)

    try:
        with urlopen(request) as response:
            raw = response.read().decode("utf-8")
            if not raw:
                return []
            return json.loads(raw)
    except HTTPError as error:
        details = error.read().decode("utf-8")
        raise RuntimeError(f"Supabase request failed ({error.code}): {details}") from error
    except URLError as error:
        raise RuntimeError(f"Supabase connection failed: {error.reason}") from error


def _normalize_book(book):
    normalized = dict(book)
    for field in DATE_FIELDS:
        value = normalized.get(field)
        if isinstance(value, str):
            try:
                normalized[field] = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                pass
    return normalized


def check_connection():
    return _request("GET", "books", "select=book_id&limit=1")


def get_books(search_term=""):
    if search_term:
        escaped = quote(f"%{search_term}%")
        query = (
            "select=book_id,title,author,isbn,quantity,borrowed_time,return_time"
            f"&or=(title.ilike.{escaped},author.ilike.{escaped},isbn.ilike.{escaped})"
            "&order=book_id"
        )
    else:
        query = (
            "select=book_id,title,author,isbn,quantity,borrowed_time,return_time"
            "&order=book_id"
        )

    response = _request("GET", "books", query)
    return [_normalize_book(book) for book in response or []]


def add_book(book_id, title, author, isbn, quantity):
    payload = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "isbn": isbn,
        "quantity": int(quantity),
        "borrowed_time": None,
        "return_time": None,
    }
    return _request("POST", "books", payload=[payload], headers=_headers("return=representation"))


def delete_book(book_id):
    query = f"book_id=eq.{quote(str(book_id))}"
    return _request("DELETE", "books", query, headers=_headers("return=representation"))


def get_book_by_id(book_id):
    query = f"select=book_id,quantity&book_id=eq.{quote(str(book_id))}&limit=1"
    rows = _request("GET", "books", query)
    return rows[0] if rows else None


def update_book(book_id, values):
    query = f"book_id=eq.{quote(str(book_id))}"
    return _request("PATCH", "books", query, payload=values, headers=_headers("return=representation"))


def authenticate_user(role, username, password):
    if role == "User":
        query = (
            "select=*"
            f"&username=eq.{quote(username)}"
            f"&password=eq.{quote(password)}"
            "&limit=1"
        )
        rows = _request("GET", "users", query)
    else:
        query = (
            "select=*"
            f"&admin_username=eq.{quote(username)}"
            f"&admin_password=eq.{quote(password)}"
            "&limit=1"
        )
        rows = _request("GET", "admins", query)
    return rows[0] if rows else None


def register_user(role, username, password):
    if role == "User":
        payload = [{"username": username, "password": password}]
        return _request("POST", "users", payload=payload, headers=_headers("return=representation"))

    payload = [{"admin_username": username, "admin_password": password}]
    return _request("POST", "admins", payload=payload, headers=_headers("return=representation"))
