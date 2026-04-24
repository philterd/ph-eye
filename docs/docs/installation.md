# Installation and Running

Ph-Eye can be run using Docker or directly from the source code.

## Running with Docker

The easiest way to run Ph-Eye is using the official Docker image.

### Pull and Run

```bash
docker run -p 5000:5000 philterd/ph-eye:latest
```

Note: The container internally listens on port 5000 by default (via `run.sh`).

### Environment Variables

- `MODEL_NAME`: The name of the GLiNER model to use. Defaults to `philterd/ph-eye-pii-base`.

Example:

```bash
docker run -p 5000:5000 -e MODEL_NAME="philterd/ph-eye-pii-base" philterd/ph-eye:latest
```

## Running from Source

### Prerequisites

- Python 3.9+
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/philterd/phileas.git
   cd ph-eye
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the service:
   ```bash
   python app.py
   ```

The service will be available at `http://localhost:5000`.
