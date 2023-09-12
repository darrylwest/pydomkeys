
project := "pydomkeys"

export PYTHONPATH := "pydomkeys/"

alias cov := cover
alias form := format
alias pre := precommit
alias todo := todos

# run the standard tests (default target)
test:
    poetry run pytest --cov=pydomkeys/ --cov-branch tests/

# run the standard tests + clippy and fmt
cover:
    poetry run coverage report -m
    poetry run coverage html --title="PyDomKeys Test Coverage"

format:
    black pydomkeys/ tests/
    isort pydomkeys/
    poetry run ruff check --fix ./pydomkeys/

ruff:
    poetry run ruff check ./pydomkeys/

lint:
    poetry run ruff check ./pydomkeys/
    poetry run pylint ./pydomkeys/

todos:
    rg TODO pydomkeys/*.py tests/*.py

mypy:
    poetry run mypy pydomkeys/

refurb:
    poetry run refurb pydomkeys/ tests/

doctest:
    poetry run python -m doctest pydomkeys/*.py
    echo "\033[32;1;4mdoctest ok\033[0m"

docs:
    poetry run sphinx-multiversion docs ./docs/_build/html

precommit:
    clear
    just test cover format ruff doctest refurb mypy

