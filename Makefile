PROJECT_NAME=weather_service
ENV_PATH=/.env

# colors
RED=$(if $(filter $(OS),Windows_NT),,$(shell    echo "\033[31m"))
GREEN=$(if $(filter $(OS),Windows_NT),,$(shell  echo "\033[32m"))
YELLOW=$(if $(filter $(OS),Windows_NT),,$(shell echo "\033[33m"))
BOLD=$(if $(filter $(OS),Windows_NT),,$(shell   echo "\033[1m"))
GRAY=$(if $(filter $(OS),Windows_NT),,$(shell    echo "\033[37m"))
RESET=$(if $(filter $(OS),Windows_NT),,$(shell    echo "\033[0m"))

## Install pre-commit hooks.
install-hooks:
	pre-commit install --hook-type pre-commit
	pre-commit install --hook-type commit-msg
	pre-commit install --install-hooks

## pre-commit
check:
	@echo '${GREEN}Checking Linters${RESET}'
	pre-commit run --all-files


# Helpers

clean:
	@find ${PROJECT_NAME}/ -name '*.pyc' -exec rm -f {} \;
	@find ${PROJECT_NAME}/ -name '__pycache__' -exec rm -rf {} \;
	@find ${PROJECT_NAME}/ -name 'Thumbs.db' -exec rm -f {} \;
	@find ${PROJECT_NAME}/ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
