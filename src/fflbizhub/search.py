# fflbizhub/search.py
from typing import Dict, Any, Iterable, List, Union
import json
import httpx

from .endpoints import ENDPOINTS

def _coerce_json(obj: Union[str, dict, list]) -> Union[dict, list]:
    if isinstance(obj, (dict, list)):
        return obj
    try:
        return json.loads(obj)
    except Exception:
        preview = obj[:200] + ("..." if len(obj) > 200 else "")
        raise RuntimeError(f"Expected JSON but got string: {preview}")

async def ad_search_page_stream(
    client: httpx.AsyncClient,
    headers: Dict[str, str],
    body: Dict[str, Any],
    url: str | None = None,
) -> Iterable[List[Dict[str, Any]]]:
    """
    Async generator yielding rows from /api/adSearch/getDataByFilter.
    Handles pagination and response shapes (dict/list or JSON string).
    """
    if url is None:
        url = ENDPOINTS["ad_search"]

    payload = json.loads(json.dumps(body))  # defensive copy
    while True:
        r = await client.post(url, json=payload, headers=headers, timeout=httpx.Timeout(60.0))
        # try JSON first, then fall back to text->json
        try:
            data = r.json()
        except Exception:
            data = r.text

        data = _coerce_json(data)

        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            rows = data.get("adBookDatas") or data.get("items") or data.get("data") or []
        else:
            raise RuntimeError(f"Unexpected response type: {type(data)}")

        yield rows

        page_size = payload["pagingParams"]["take"]
        if len(rows) < page_size:
            break
        payload["pagingParams"]["skip"] += page_size

