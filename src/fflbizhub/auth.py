import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import requests


class FFLBizHubAuth:
    """
    Authenticates a user and manages FFL tokens + user-scoped data for Orchid FFLBizHub.

    - Retrieves and caches an auth token
    - Automatically refreshes token if expired (based on local cache TTL)
    - Retrieves list of associated FFLs on login and caches it
    """

    def __init__(
        self,
        email: str,
        password: str,
        cache_file: str | Path = "ffl_token.json",
        ffls_file: str | Path = "ffl_books.json",
        base_url: str = "https://app.fflbizhub.com",
        ttl: timedelta = timedelta(days=6, hours=12),  # assume ~7-day token
    ) -> None:
        self.email = email
        self.password = password
        self.cache_file = Path(cache_file)
        self.ffls_file = Path(ffls_file)
        self.base_url = base_url.rstrip("/")
        self.auth_url = f"{self.base_url}/api/auth"
        self.ffls_url = f"{self.base_url}/api/multiBookSearch/getUserFFLs"
        self.ttl = ttl
        self.token: Optional[str] = None

    def _login(self) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=utf-8",
            "userTimezone": "Central Daylight Time",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/portal/login",
        }
        payload = {"email": self.email, "password": self.password}
        resp = requests.post(self.auth_url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data: Dict[str, Any]
        if resp.headers.get("content-type", "").startswith("application/json"):
            data = resp.json()
        else:
            data = json.loads(resp.text)
        token = data.get("token")
        if not token:
            raise ValueError("No token returned from API.")
        return token

    def _load_cached_token(self) -> Optional[str]:
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "r") as f:
                    data = json.load(f)
                if datetime.strptime(data["expires_at"], "%Y-%m-%dT%H:%M:%S") > datetime.utcnow():
                    return data["token"]
        except Exception:
            pass
        return None

    def _cache_token(self, token: str) -> None:
        expiration = datetime.utcnow() + self.ttl
        with open(self.cache_file, "w") as f:
            json.dump(
                {"token": token, "expires_at": expiration.strftime("%Y-%m-%dT%H:%M:%S")},
                f,
            )

    def _fetch_and_cache_ffls(self, token: str) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "X-Auth-Token": token,
            "userTimezone": "Central Daylight Time",
            "Referer": f"{self.base_url}/portal/ead/openassignments",
        }
        resp = requests.get(self.ffls_url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json() if resp.headers.get("content-type","").startswith("application/json") else json.loads(resp.text)
        with open(self.ffls_file, "w") as f:
            json.dump(data, f, indent=2)
        return data

    def get_token(self, force_refresh: bool = False) -> str:
        if not force_refresh:
            cached = self._load_cached_token()
            if cached:
                self.token = cached
                return cached
        new_token = self._login()
        self._cache_token(new_token)
        try:
            self._fetch_and_cache_ffls(new_token)
        except Exception:
            pass
        self.token = new_token
        return new_token

