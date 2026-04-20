# Job Search API

A FastAPI service that scrapes LinkedIn job posts via Apify.

## Setup

### Environment Variables

| Variable | Description |
|---|---|
| `APIFY_API_TOKEN` | Your Apify API token |

### Run Locally

```bash
uvicorn main:app --port 8000
```

### Run with Docker

```bash
docker build -t job-search .
docker run -p 8000:8000 -e APIFY_API_TOKEN=your_token job-search
```

## API Reference

### POST `/run-actor`

Search LinkedIn posts for job listings.

**Request Body**

| Field | Type | Default | Description |
|---|---|---|---|
| `keyword` | string | `""` | Search keyword |
| `sort_type` | string | `"relevance"` | `relevance` or `recent` |
| `page_number` | int | `1` | Page number |
| `date_filter` | string | `""` | e.g. `r86400` for last 24h |
| `limit` | int | `50` | Max results |
| `company_urns` | string | `null` | Filter by company URN |
| `author_company_urns` | string | `null` | Filter by author's company URN |
| `author_industry_urns` | string | `null` | Filter by author's industry URN |
| `author_job_title` | string | `null` | Filter by author job title |
| `member_urns` | string | `null` | Filter by member URN |
| `total_posts` | int | `null` | Total posts to fetch |

**Sample Request**

```http
POST http://localhost:8000/run-actor
Content-Type: application/json

{
  "keyword": "python developer",
  "sort_type": "recent",
  "limit": 10,
  "date_filter": "r86400"
}
```

**Sample Response**

```json
{
  "actorName": "apify-run-abc123",
  "runId": "xyz789",
  "defaultDatasetId": "dataset456",
  "items": [
    {
      "activity_id": "7451922721392824320",
      "post_url": "https://www.linkedin.com/posts/...",
      "text": "Hiring: Python Developer...",
      "author": {
        "name": "Jane Doe",
        "headline": "Recruiter at Acme Corp",
        "profile_url": "https://www.linkedin.com/in/janedoe"
      },
      "stats": {
        "total_reactions": 12,
        "comments": 3,
        "shares": 1
      },
      "posted_at": {
        "display_text": "2h",
        "date": "2026-04-20 14:00:00"
      }
    }
  ]
}
```

## Deploy on Render

1. Push this repo to GitHub
2. On Render → **New** → **Web Service** → connect your repo
3. Set **Environment** to `Docker`
4. Add environment variable: `APIFY_API_TOKEN`
