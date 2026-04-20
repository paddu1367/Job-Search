import os
import uuid
from typing import Optional

from apify_client import ApifyClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise RuntimeError("Please set APIFY_API_TOKEN environment variable")

client = ApifyClient(APIFY_API_TOKEN)

class ActorInput(BaseModel):
    keyword: str = ""
    sort_type: str = "relevance"
    page_number: int = 1
    date_filter: str = ""
    limit: int = 50
    company_urns: Optional[str] = None
    author_company_urns: Optional[str] = None
    author_industry_urns: Optional[str] = None
    author_job_title: Optional[str] = None
    member_urns: Optional[str] = None
    total_posts: Optional[int] = None

@app.post("/run-actor")
def run_actor(input: ActorInput):
    actor_name = f"apify-run-{uuid.uuid4().hex}"
    run_input = {k: v for k, v in input.model_dump().items() if v is not None}
    run_input["actor_name"] = actor_name

    try:
        run = client.actor("5QnEH5N71IK2mFLrP").call(run_input=run_input)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if not isinstance(run, dict) or "defaultDatasetId" not in run:
        return {"actorName": actor_name, "run": run, "items": []}

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    return {
        "actorName": actor_name,
        "runId": run.get("id"),
        "defaultDatasetId": run.get("defaultDatasetId"),
        "items": items,
    }
