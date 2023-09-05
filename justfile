
project := "pydomkeys"

export PYTHONPATH := "pydomkeys/"

alias t := test
alias cov := cover
alias form := format
alias pre := precommit

# run the standard tests
test:
    poetry run pytest --cov=pydomkeys/ --cov-branch

# run the standard tests + clippy and fmt
cover:
    poetry run coverage report -m
    coverage html --title="Logging Service Test Coverage"

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


precommit:
    just test
    just cover
    just format
    just ruff
    just mypy

