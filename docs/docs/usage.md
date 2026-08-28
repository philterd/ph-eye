# API Usage

Ph-Eye provides two endpoints: `GET /health` and `POST /find`.

## Health check

**Endpoint:** `GET /health`

Returns a standard JSON health response when the service is running and the model is loaded.

**Example request:**

```bash
curl http://localhost:5000/health
```

**Example response:**

```json
{
  "status": "UP",
  "applicationVersion": "1.3.0"
}
```

## Find entities

**Endpoint:** `POST /find`

Finds entities in the provided text.

### Request body

| Field       | Type            | Required | Description                                                                                                  |
|-------------|-----------------|----------|--------------------------------------------------------------------------------------------------------------|
| `text`      | string          | Yes      | The text to analyze.                                                                                         |
| `labels`    | list of strings | No       | Entity labels to search for. Defaults to the model's built-in labels if omitted or empty.                    |
| `threshold` | float           | No       | Minimum confidence score for a result to be returned. Defaults to the model's built-in threshold if omitted. |

Default values for `labels` and `threshold` vary by model — see [Available models](index.md#available-models).

### Example request

```bash
curl -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d '{
    "text": "George Washington was president and he lived in Virginia.",
    "labels": ["Person", "Place"],
    "threshold": 0.5
  }'
```

### Example response

```json
[
  {
    "label": "Person",
    "text": "George Washington",
    "score": 0.9923100471496582,
    "start": 0,
    "end": 17
  },
  {
    "label": "Place",
    "text": "Virginia",
    "score": 0.9528881907463074,
    "start": 48,
    "end": 56
  }
]
```

### Response fields

| Field   | Type   | Description                                            |
|---------|--------|--------------------------------------------------------|
| `label` | string | The entity type.                                       |
| `text`  | string | The matched text span.                                 |
| `score` | float  | Confidence score between 0 and 1.                      |
| `start` | int    | Start character offset of the match in the input text. |
| `end`   | int    | End character offset of the match in the input text.   |
