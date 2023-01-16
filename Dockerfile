FROM python:3.10.4 AS builder

WORKDIR /seller_products
COPY poetry.lock pyproject.toml ./
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN python -m venv .venv && \
    export PATH="/seller_products/.venv/bin:${HOME}/.local/bin:${PATH}" && \
    poetry install --only main
COPY . .

FROM python:3.10.4-slim AS final

WORKDIR /seller_products
COPY --from=builder /seller_products/.venv .venv
ENV PATH="/seller_products/.venv/bin:${PATH}"
RUN apt update && apt install -y libpq5
COPY . .

ENTRYPOINT ["sh", "./scripts/entrypoint.sh"]