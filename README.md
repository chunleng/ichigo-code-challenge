# Ichigo Code Challenge

Code Challenge for Ichigo Job Application

## Quickstart

Start up easily with docker-compose

```sh
cd /ichigo-code-challenge
docker-compose up
```

Frontend pages

- <http://localhost:33000/1/loyalty>
- <http://localhost:33000/1/order>

API

- <http://localhost:38000/docs>

## Project Struture

```txt
.
├─ apps (application code)
│  ├─ front
│  └─ api
└─ docker-compose.yml
```

## Development

### Prerequisites

- Python
  * Install pyenv <https://github.com/pyenv/pyenv>
  * Go to `apps/backend`, install poetry onto the pyenv managed Python
    <https://github.com/python-poetry/poetry>
- Node
  * Install nodenv <https://github.com/nodenv/nodenv>
- Docker <https://www.docker.com/>
- Direnv <https://github.com/direnv/direnv>

### Setup

```sh
make
```

### Run

To get the project running, the following resources are required

```sh
make dev-front
make dev-api
make dev-resources
```

Other commands are also available in `Makefile`
