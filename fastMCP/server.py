from fastmcp import FastMCP
import httpx

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

mcp = FastMCP("[fastmcp] weather")


# Helper function to call the NWS API
async def make_nws_request(url: str) -> dict | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Error fetching NWS data: {e}")
        return None


# Format alert data to readable string
def format_alert(feature: dict) -> str:
    props = feature.get("properties", {})
    return "\n".join(
        [
            f"Event: {props.get('event', 'Unknown')}",
            f"Area: {props.get('areaDesc', 'Unknown')}",
            f"Severity: {props.get('severity', 'Unknown')}",
            f"Status: {props.get('status', 'Unknown')}",
            f"Headline: {props.get('headline', 'No headline')}",
            "---",
        ]
    )


@mcp.tool
async def get_alerts_fastMCP(state: str) -> dict:
    """Get weather alerts for a given US state (e.g. CA, NY)."""

    state = state.upper()
    print(f"✅ get-alerts-fastmcp with state = {state}")

    url = f"{NWS_API_BASE}/alerts?area={state}"
    data = await make_nws_request(url)
    features = data.get("features", []) if data else []

    if not features:
        msg = (
            f"No active alerts for {state}"
            if data
            else "Failed to retrieve alerts data"
        )
        return {"content": [{"type": "text", "text": msg}]}

    alerts = "\n".join(format_alert(f) for f in features)
    return {
        "content": [{"type": "text", "text": f"Active alerts for {state}:\n\n{alerts}"}]
    }


if __name__ == "__main__":
    mcp.run()
