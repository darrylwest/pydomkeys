
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

# format the code with black, isort and ruff --fix
format:
    black pydomkeys/ tests/
    isort pydomkeys/
    poetry run ruff check --fix ./pydomkeys/

# run ruff linter
ruff:
    poetry run ruff check ./pydomkeys/

# run the ruf and pylint linters
lint:
    poetry run ruff check ./pydomkeys/
    poetry run pylint ./pydomkeys/

# dump out the list of todos
todos:
    rg TODO pydomkeys/*.py tests/*.py

# run mypy to check typing
mypy:
    poetry run mypy pydomkeys/

# run refurb to find alternative coding patterns
refurb:
    poetry run refurb pydomkeys/ tests/

# run the stress tests
stress:
    poetry run ./tests/stress.py

# run the doc tests
doctest:
    poetry run python -m doctest pydomkeys/*.py
    @echo "\033[32;1;4mdoctest ok\033[0m"

# create the sphinx multiversion docs
docs:
    poetry run sphinx-multiversion docs ./docs/_build/html

# run all the pre-commit jobs
precommit:
    clear
    just test cover stress format ruff doctest refurb mypy

