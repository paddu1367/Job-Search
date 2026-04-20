import requests

payload = {
    "keyword": "python developer",
    "sort_type": "relevance",       # relevance | recent
    "page_number": 1,
    "date_filter": "",              # e.g. "r86400" for last 24h
    "limit": 10,
    # "company_urns": "",
    # "author_company_urns": "",
    # "author_industry_urns": "",
    # "author_job_title": "",
    # "member_urns": "",
    # "total_posts": None,
}

response = requests.post("http://localhost:8000/run-actor", json=payload)
data = response.json()

print(f"Run ID: {data.get('runId')}")
print(f"Items returned: {len(data.get('items', []))}")
for item in data.get("items", []):
    print(f"\n- {item['author']['name']}: {item['text'][:100]}...")
