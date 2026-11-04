# Latch OIDC

An OpenID Connect identity provider built with Python and FastAPI, with TypeScript/Next.js client apps planned to demonstrate single sign-on.

I’m building Latch to understand the parts of authentication that an SDK usually handles: browser redirects, sessions, authorization codes, token validation, and revocation. The provider will implement the protocol flow directly and use established libraries for cryptography and password hashing.

## Status

Early development. The HTTP foundation works; authentication is not implemented yet.

Currently implemented:

- HTML home page and JSON liveness endpoint.
- Request logging that omits query parameters.
- Tests for responses, unknown routes, unsupported methods, and logging.
- Static type checking with mypy.

Next: registration, password hashing, and database-backed sessions. After that: Authorization Code Flow with PKCE, signed tokens, discovery/JWKS, consent, refresh-token rotation, and two independent client apps.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.12, then:

```sh
git clone https://github.com/aegloist/latch-oidc.git
cd latch-oidc/apps/idp
uv sync --locked
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 4000 --no-access-log
```

Open [localhost:4000](http://localhost:4000). The liveness endpoint is [`/health/live`](http://localhost:4000/health/live); it returns `{"status":"ok"}`. FastAPI’s interactive API docs are at `/docs`.

`--reload` restarts the server after edits. Raw Uvicorn access logs are disabled because URLs may eventually contain authorization codes. The application logs the method, route pattern, and response status instead.

## Checks

From `apps/idp`:

```sh
uv run pytest
uv run mypy
```

Tests exercise the FastAPI application through its in-process test client. They do not require a running server or database.

## Layout

```text
apps/idp/
  app/main.py       Application and request handlers
  tests/            HTTP behavior tests
  pyproject.toml    Dependencies and tool configuration
  uv.lock           Locked dependency versions
```

The backend uses Python 3.12, FastAPI, and Uvicorn. uv manages the environment; pytest checks behavior and mypy checks types. PostgreSQL and the Next.js clients will be added when those features are implemented.

## Reference

Inspired by [Atharv Dange’s Kleis OIDC](https://github.com/atharvdange618/OIDC). Latch follows the same project idea with a Python provider implementation. Protocol work will follow [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html) and [OAuth security best practices](https://www.rfc-editor.org/rfc/rfc9700.html).

This project is under development and is not ready to manage production identities.
