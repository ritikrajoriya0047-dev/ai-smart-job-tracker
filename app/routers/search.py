from fastapi import APIRouter, HTTPException
import requests, os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/search", tags=["Job Search"])

# --- Helper Functions ---

def _parse_adzuna_response(data: dict) -> list[dict]:
    """Parse and flatten the complex Adzuna JSON response into our normalized schema."""
    jobs_list = []
    for item in data.get("results", []):
        jobs_list.append({
            "title": item.get("title"),
            "company": item.get("company", {}).get("display_name"),
            "location": item.get("location", {}).get("display_name"),
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "description": item.get("description", "")[:200], # Truncate to keep payload small
            "url": item.get("redirect_url"),
            "created": item.get("created")
        })
    return jobs_list


@router.get("/")
def search_jobs(q: str, location: str = "india", results: int = 10):
    """
    Search for jobs using the external Adzuna API.
    """
    app_id  = os.getenv("ADZUNA_APP_ID")
    api_key = os.getenv("ADZUNA_API_KEY")

    if not app_id or not api_key:
        raise HTTPException(status_code=500, detail="Adzuna API keys not configured")

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": app_id,
        "app_key": api_key,
        "what": q,
        "where": location,
        "results_per_page": results,
        "content-type": "application/json"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Adzuna API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    # Delegate the messy parsing to a helper function
    jobs_list = _parse_adzuna_response(data)
        
    return {
        "query": q,
        "location": location,
        "total_found": data.get("count", 0),
        "results": jobs_list
    } 