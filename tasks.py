from invoke import task

PORT = 8000

@task
def install(c):
    """Установка зависимостей"""
    c.run("uv sync")

@task
def dev(c, port=PORT):
    """Запуск сервера"""
    c.run(f"uv run uvicorn src.main:app --reload --port {port}", env={"PYTHONIOENCODING": "utf-8"})

@task
def test(c):
    """Запуск тестов"""
    c.run("uv run pytest")

@task
def lint(c):
    """Проверка кода"""
    c.run("uv run ruff check .")

@task
def format(c):
    """Форматирование кода"""
    c.run("uv run ruff format .")

@task
def clean(c):
    """Очистка временных файлов"""
    import os
    import shutil
    
    folders = [".venv", ".pytest_cache", ".ruff_cache", "__pycache__"]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)