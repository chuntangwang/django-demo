# Django Demo

## Prerequisite

* [mise](https://github.com/jdx/mise)
* [uv](https://github.com/astral-sh/uv)

**Install uv**

```shell
mise use --global uv
```

### Create project

Create project with uv
```shell
# create init project with uv
uv init django-demo
cd django-demo
# add dependencies
uv add django djangorestframework markdown django-filter
# activiate venv
source .venv/bin/activate
# create django project
django-admin startproject mysite .
```

Run server

```shell
uv run manage.py runserver
# CTRL-c to stop
```

### Test framework

Install [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html) for dev

```
uv add --dev pytest-django
```

Setup configuration in `pyproject.toml`

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "mysite.settings"
python_files = [
    "tests/test_*.py"
]
```

Run tests

```shell
> pytest
=== test session starts ===
platform darwin -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0
django: version: 5.1.4, settings: mysite.settings (from ini)
rootdir: <path>/django-demo
configfile: pyproject.toml
plugins: django-4.9.0
collected 0 items
=== no tests ran in 0.23s ===
```

### Linter

Install [ruff](https://github.com/astral-sh/ruff) for dev

```shell
uv add --dev ruff

# lint all files
ruff check
# check format
ruff format --check
# check format and diff
ruff format --diff
# format
ruff format
```
