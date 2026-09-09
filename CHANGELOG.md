## 1.3.0 (unreleased)

- Changed the default English PII model to `pii_en_small` (`philterd/ph-eye-pii-en-small`), superseding `pii_base` (`philterd/ph-eye-pii-base`). The new model detects person names using the single label `name` at a default threshold of `0.90`.
- Because this is a different statistical model, detections on identical input will differ from `ph-eye-pii-base`: which names are found (in both directions), entity boundaries, the label string (`name` instead of `Person`), and confidence scores. This is expected when changing a detector, not a bug. Re-validate against representative data from your own pipeline rather than assuming parity.
- Added the rest of the English name model size ladder as selectable models: `pii_en_xsmall`, `pii_en_medium`, and `pii_en_large` (alongside the default `pii_en_small`). All use the label `name` with size-specific default thresholds (0.50, 0.90, 0.70, 0.95 for xsmall, small, medium, large).
- Pinned the Hugging Face revision for each `ph-eye-pii-en-*` model so Docker builds are reproducible and air-gapped at runtime. A new `MODEL_REVISION` environment variable can override it.
- Deprecated the `pii_base` model module. It still loads `ph-eye-pii-base` when explicitly selected with `PHEYE_MODEL=pii_base`, but it is no longer the default and may be removed in a future release. To keep the previous behavior temporarily, pin `PHEYE_MODEL=pii_base`.
- The `latest` Docker tag (and `latest-gpu`) now points at the default `pii_en_small` model, so `docker pull philterd/ph-eye` gets the new default English model.
- Renamed the health check endpoint from `/status` to `/health`.

## 1.2.5 (2026-05-26)

- Consolidated all model variants into a single codebase and repository. Previously each model lived on a separate branch; models now live in `models/` as individual modules.
- Added support for all models in a single Docker image build process controlled by the `PHEYE_MODEL` build argument.
- Added models: `medical_conditions` (English disease/disorder via `blaze999/Medical-NER`) and `french_medical` (French disease via `almanach/camembert-bio-gliner-v0.1`).
- Added `docker-compose.yaml` with a service per model.
- Added `Dockerfile.gpu` for GPU-enabled deployments using `pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime` as the base image.
- Pinned `transformers` explicitly for the first time, ending the release at `transformers[torch]==5.1.0`. GLiNER had previously selected it transitively.
- Pinned `waitress` to an exact version (`==3.0.2`).

## 1.2.4

Not a release of this image. Version 1.2.4 belongs to `philterd/ph-eye-fr-persons`, which was built from its own branch. See "Model variant images" below.

## 1.2.3 (2026-05-26)

- Added documentation.
- Updated Flask to 3.1.3.
- Updated GLiNER to 0.2.26.

## 1.2.2 (2025-11-02)

- Dependency updates.

## 1.2.1 (2024-11-20)

- Added script to run the Docker image.
- Added model-loaded confirmation to startup log output.
- Added documentation.

## 1.2.0 (2024-11-19)

- Switched from Flask development server to waitress as the production WSGI server.
- Added error handling to the `/find` endpoint.
- Removed unused `mpmath` import.

## 1.1.0 (2024-11-19)

- Switched default model from `urchade/gliner_mediumv2.1` to `philterd/ph-eye-pii-base`.

## 1.0.0 (2024-09-24)

- Initial release.
- REST API with `/status` and `/find` endpoints.
- GLiNER-based zero-shot NER.
- Dockerized with build-time model download.
- Configurable model via `MODEL_NAME` environment variable.
- Default label fallback when no labels are provided.

## Model variant images

Before the 1.2.5 consolidation, each model shipped from its own branch to its own Docker
repository. Version numbers were per repository and independent of `philterd/ph-eye`, so
the same number can appear on more than one image. Those branches are archived under the
`archive/*` tags.

| Image | Version | Archived branch | Last commit |
| --- | --- | --- | --- |
| `philterd/ph-eye-medical-conditions` | 1.2.3 | `archive/medical-conditions` | `f57197c` (2026-01-20) |
| `philterd/ph-eye-fr-medical` | 1.2.3 | `archive/french-medical` | `1f8bd25` (2026-02-04) |
| `philterd/ph-eye-fr-persons` | 1.2.4 | `archive/french-persons` | `87f5c6a` (2026-02-24) |
| `philterd/ph-eye-hospitals` | 1.2.5 | `archive/hospitals` | `a75522c` (2026-02-24) |

The hospitals model (`knowledgator/gliner-pii-base-v1.0`) and the French persons model
(`EmergentMethods/gliner_medium_news-v2.1`) were released from those branches, not from
`main`.

The 1.2.3 and 1.2.5 tags were created retroactively at the last commit carrying each
version in `app.py`. The dates shown are that commit's date, not a confirmed publish date;
no tag recorded which tree each published image was built from.
