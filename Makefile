install-precommit:
	pre-commit install

install-virtualenv:
	poetry install

poetry-lock:
	poetry lock

poetry-add:
	poetry add $(package)

poetry-remove:
	poetry remove $(package)

run-black:
	poetry run black src --check
	poetry run black tests --check

run-flake8:
	poetry run flake8 src
	poetry run flake8 tests

run-isort:
	poetry run isort src --check
	poetry run isort tests --check

run-ci: run-black run-isort run-flake8

run-pytest:
	PYTHONPATH=./src/ poetry run pytest

run-processing-script:
	poetry run python src/process_survey_results.py