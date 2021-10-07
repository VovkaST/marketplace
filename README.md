###  Не обязательное, но желательный инструмент.

Git-hook позволит вам содержать код в определнном стиле.

Этот инструмент, при небольшой доработке позволит отправлять уведомления, или делать тесты.

Автоматизировать рутинные задачи, которые вы исполняли перед коммитами.

### Краткая инструкция по установке


```bash
pip install black isort pre-commit flake8

# добавляем файлы конфигурации

pre-commit install

# эта комманда добавить в git hooks новый скрипт.
# кстати сами скрпты можно найти в ./.git/hooks/
```

Будут нужны еще файлы конфигурации для black, flake8 и pre-commit


#### pre-commit-config.yaml
```yaml

repos:
  - repo: https://github.com/pycqa/isort
    rev: 5.8.0
    hooks:
      - id: isort
        name: isort (python)
  - repo: https://github.com/ambv/black
    rev: stable
    hooks:
    - id: black
      language_version: python3.6
  - repo: https://gitlab.com/pycqa/flake8
    rev: 3.7.9
    hooks:
    - id: flake8  

```

#### .toml для black
```ini

[tool.black]
line-length = 79
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
''' 

```

#### .flake8
```ini

[flake8]
ignore = E203, E266, E402, E501, W503, F403, F401
max-line-length = 79
max-complexity = 18
select = B,C,E,F,W,T4,B9

```
