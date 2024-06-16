# Skillometer API

![made_by](https://img.shields.io/badge/made_by-IDEV-0d9488.svg?style=flat-square)

## Parts

- [root](https://github.com/idev-present/skillometer)
- [API](https://github.com/idev-present/skillometer-api)
- [WEB admin](https://github.com/idev-present/skillometer-web-admin)
- [TWA client](https://github.com/idev-present/skillometer-app-client)

### Requirements

- docker
- docker compose

## Local setup

1. Copy env `cp .env.development .env`. Setup secrets (change `changethis` in `.env`)
2. Up database container `docker compose -f docker-compose.local.yml up --build -d`
3. Setup python version `pyenv global 3.12`
4. Setup virtual environment `poetry env use 3.12`
5. Install deps `poetry install`
6. Activate virtual environments `poetry shell`
7. Setup base dir for scripts `export PYTHONPATH=.`
8. Check db connect `python app/scripts/pre_start.py`
9. Apply database migration `alembic upgrade head`
10. Load fixtures for dictionaries `python app/script/load_fixtures.py`
11. Run dev server `fastapi dev`
12. Profit!

## Build && Deploy

```shell
export TAG=0.3.1
docker compose -f docker-compose.builder.yml build && docker compose -f docker-compose.builder.yml push
```

## Configuration

### Env variables

See kubernetes config `provision/deployment.values`

## Authors

| Name            | Email                                                                     | Social                            |
|-----------------|---------------------------------------------------------------------------|-----------------------------------|
| Ilya Zhuravlev  | [ilya.zhuravlev@idev-present.com](mailto:ilya.zhuravlev@idev-present.com) | [telegram](https://t.me/ichiro18) |
| Maxim Araslanov | [ilya.zhuravlev@idev-present.com](mailto:ilya.zhuravlev@idev-present.com) | [telegram](https://t.me/ichiro18) |

