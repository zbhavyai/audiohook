FROM docker.io/library/python:3.14-slim
ARG REVISION
LABEL org.opencontainers.image.title="AudioHook"
LABEL org.opencontainers.image.description="AudioHook"
LABEL org.opencontainers.image.source="https://github.com/zbhavyai/audiohook"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Bhavyai Gupta <https://zbhavyai.github.io>"
LABEL org.opencontainers.image.version="${REVISION}"
WORKDIR /opt/app
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${REVISION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/app \
    PATH="/opt/app/.venv/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-group dev
ENTRYPOINT ["python", "-m", "src"]
CMD []
