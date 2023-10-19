'''
task runner, @see https://www.pyinvoke.org/
'''

from invoke import task

@task
def test(ctx):
    ctx.run('poetry run pytest --cov=pydomkeys/ --cov-branch tests/', pty=True)

@task(aliases=['cov'])
def cover(ctx):
    ctx.run('poetry run coverage report -m', pty=True)
    ctx.run('poetry run coverage html --title="PyDomKeys Test Coverage"', pty=True)

@task(name='format', aliases=['black','isort'])
def formatter(ctx):
    ctx.run('black pydomkeys/ tests/', pty=True)
    ctx.run('isort pydomkeys/', pty=True)
    ctx.run('poetry run ruff check --fix ./pydomkeys/', pty=True)

@task
def ruff(ctx):
    ctx.run('poetry run ruff check ./pydomkeys/', pty=True)

@task
def lint(ctx):
    ctx.run('poetry run ruff check ./pydomkeys/', pty=True)
    ctx.run('poetry run pylint ./pydomkeys/', pty=True)

@task(aliases=['todo'])
def todos(ctx):
    ctx.run('rg TODO pydomkeys/*.py tests/*.py', pty=True)

@task
def mypy(ctx):
    ctx.run('poetry run mypy pydomkeys/', pty=True)

@task
def refurb(ctx):
    ctx.run('poetry run refurb pydomkeys/ tests/', pty=True)

@task
def stress(ctx):
    ctx.run('poetry run ./tests/stress.py', pty=True)

@task
def doctest(ctx):
    ctx.run('poetry run python -m doctest pydomkeys/*.py', pty=True)
    ctx.run('echo "\033[32;1;4mdoctest ok\033[0m"', pty=True)

@task
def docs(ctx):
    ctx.run('poetry run sphinx-multiversion docs ./docs/_build/html', pty=True)

@task
def repl(ctx):
    ctx.run('poetry run bpython -i .repl-start.py', pty=True)

@task(aliases=['precommit'])
def pre(ctx):
    ctx.run('clear', pty=True)
    test(ctx)
    cover(ctx)
    stress(ctx)
    formatter(ctx)
    ruff(ctx)
    doctest(ctx)
    refurb(ctx)
    mypy(ctx)

