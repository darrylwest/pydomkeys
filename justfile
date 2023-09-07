
project := "pydomkeys"

export PYTHONPATH := "pydomkeys/"

alias cov := cover
alias form := format
alias pre := precommit

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
    refurb pydomkeys/ tests/

precommit:
    clear
    just test cover format ruff refurb mypy

