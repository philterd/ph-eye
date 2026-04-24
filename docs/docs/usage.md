# API Usage

Ph-Eye provides two main endpoints: `/status` and `/find`.

## Health Check

**Endpoint:** `GET /status`

Returns the health status of the service and the name of the model currently in use.

**Example Request:**

```bash
curl http://localhost:5000/status
```

**Example Response:**

```
healthy: philterd/ph-eye-pii-base
```

## Find Entities

**Endpoint:** `POST /find`

Finds entities in the provided text.

### Request Body

The request body must be a JSON object with the following fields:

- `text` (required, string): The text to analyze.
- `labels` (optional, list of strings): The entity labels to look for. Defaults to `["Person"]`. If an empty list is provided, it also defaults to `["Person"]`.
- `threshold` (optional, float): The confidence threshold for entity detection. Defaults to `0.5`.

### Example Request

```bash
curl -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d '{
  "text": "George Washington was president and he lived in Virginia.",
  "threshold": 0.5,
  "labels": [
    "Person",
    "Place"
  ]
}'
```

### Example Response

```json
[
  {
    "end": 17,
    "label": "Person",
    "score": 0.9923100471496582,
    "start": 0,
    "text": "George Washington"
  },
  {
    "end": 56,
    "label": "Place",
    "score": 0.9528881907463074,
    "start": 48,
    "text": "Virginia"
  }
]
```
