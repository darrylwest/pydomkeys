#!/usr/bin/env bash
# dpw@plaza.localdomain
# 2023-08-10 18:46:10
#

set -eu

# read in all env vars
export PYTHONPATH=pydomkeys/

run() {
    env | fgrep LOGGING_
    echo "running the application in the background..."
    poetry run uvicorn pydomkeys.main:app --reload --host=$LOCAL_IP --port 15010
}

start() {
    echo "not ready yet--need to evaluate the env and choose staging or prod and configure rolling logs"
    exit 1

    poetry run uvicorn pydomkeys.main:app --host=$LOCAL_IP --port 15010 &
    echo "pid=$!"
}

tests() {
    echo "running tests"
    poetry run pytest --cov=pydomkeys/ --cov-branch
}

redis_tests() {
    echo "running redis tests"
    poetry run pytest -m redis
}

cover() {
    echo "coverage"
    poetry run coverage report -m
    coverage html --title="Logging Service Test Coverage"
}

format() {
    black pydomkeys/ tests/
    isort pydomkeys/
    poetry run ruff check --fix ./pydomkeys/
}

ruff() {
    echo "ruff the project and test files..."
    poetry run ruff check ./pydomkeys/
    # poetry run ruff  tests/ --per-file-ignores="tests/*:S101"
}


lint() {
    echo "pylint the project files..."
    poetry run pylint ./pydomkeys/
}

find_todos() {
    rg TODO pydomkeys/*.py pydomkeys/db/*.py tests/*.py 
}

watch() {
    # this has a bug the runs the tests 3 times for a single save; no de-bounce
    # watchmedo shell-command --patterns="src/*.py" --recursive --command='poetry run pytest tests/'
    watchexec -c -w pydomkeys/ -w tests/ -e .py -d 500 'poetry run pytest tests/ -cov=pydomkeys/'
}

run_mypy() {
    poetry run mypy pydomkeys/
}

pre_commit() {
    clear
    format

    echo "running unit and integration tests..."
    tests && integration_test 

    echo "running lint and ruff..."
    ruff

    echo "running refurb..."
    refurb pydomkeys/ tests/

    echo "running mypy..."
    run_mypy
}

show_help() {
    # todo - redo this in python to add color...
    echo "USE: mk [sub-command]"
    echo "  redis: run the redis tests in test model"
    echo "  test: run the test suite"
    echo "  inttest: run the integration test suite (server must be running)"
    echo "  cover: run the test coverage"
    echo "  lint: lint the all files"
    echo "  ruff: lint all files with ruff"
    echo "  run: run the application"
    echo "  start: start the application in the background; log it logs/logfile"
    echo "  watch: watch all files and run the tests on change"
    echo "  format: run black and isort on the project"
    echo "  precommit: run formmating, lint, tests integration prior to git commit"
    echo "  todo: show the TODOs by scanning src files"
    echo "  --help: show this help message"
}

if [[ $# -eq 0 ]]
then
    show_help
else
    key="$1"

    case $key in
        -h|--help)
            show_help
            ;;

        test|te*)
            tests
            ;;

        int*)
            integration_test
            ;;

        cov*)
            tests && cover
            ;;

        redis*)
            redis_tests
            ;;

        lint)
            ruff
            lint
            ;;

        ruff)
            ruff
            ;;

        mypy)
            run_mypy
            ;;

        black|form*)
            format
            ;;

        run)
            run
            ;;

        start)
            start
            ;;

        pre*)
            pre_commit
            ;;

        watch)
            watch
            ;;

        todo*)
            find_todos
            ;;


        *)
            show_help
            ;;
    esac
fi
