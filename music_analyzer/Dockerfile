FROM python:slim AS base

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEMUCS_MODEL=htdemucs_6s

FROM base AS builder
WORKDIR /build

# copy only build metadata first for cache‑friendly layer
COPY pyproject.toml requirements.txt ./
RUN pip install --upgrade pip build && \
    python -m build --wheel --outdir /build/dist

FROM base AS runtime
WORKDIR /app
# copy built wheel from builder
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install /tmp/*.whl && rm -rf /tmp/*.whl
# copy source (nice for stack traces & debugging)
# COPY app ./app
# # copy built wheel from builder
# COPY --from=builder /build/dist/*.whl /tmp/
# RUN pip install /tmp/*.whl && rm -rf /tmp/*.whl

ENTRYPOINT ["audio-tab-gen"]
CMD ["--input", "/input", "--output", "/output"]
# COPY app ./app

# # Default CMD: process every supported file in /input; write results to /output
# CMD find /input -maxdepth 1 -type f \( -iname "*.mp3" -o -iname "*.wav" -o -iname "*.flac" \) -print0 | \
#     xargs -0 -I {} python -m app.main --input {} --output /output
