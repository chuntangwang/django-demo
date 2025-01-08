# Django Demo

## Prerequisite

* [mise](https://github.com/jdx/mise)
* [uv](https://github.com/astral-sh/uv)

**Install uv**

```shell
mise use --global uv
```

### Create project with uv

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