from invoke.tasks import task

HOST = "127.0.0.1"
PORT = 8000
RELOAD = True


@task
def install(c):
    c.run("uv sync")


@task
def dev(c, host=HOST, port=PORT, reload=RELOAD):
    c.run(
        f"uv run uvicorn src.main:app --host {host} --port {port} {reload and '--reload'}",
        env={"PYTHONIOENCODING": "utf-8"},
    )


@task
def test(c):
    c.run("uv run pytest")


@task
def check(c):
    c.run("uv run pyright")


@task
def lint(c):
    c.run("uv run ruff check .")


@task
def format(c):
    c.run("uv run ruff format .")


@task
def clean(_):
    from os import path
    from shutil import rmtree

    folders = [".venv", ".pytest_cache", ".ruff_cache", "__pycache__"]
    for folder in folders:
        if path.exists(folder):
            rmtree(folder, ignore_errors=True)
