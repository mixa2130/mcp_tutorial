from typing import Any
import httpx

USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    res = [f"Event: {props.get('event', 'Unknown')}",
           f"Area: {props.get('areaDesc', 'Unknown')}",
           f"Severity: {props.get('severity', 'Unknown')}",
           f"Description: {props.get('description', 'No description available')}",
           f"Instructions: {props.get('instruction', 'No specific instructions provided')}"]

    return '\n'.join(res)
