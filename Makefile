.PHONY: init clean update format lint version

help: ## show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s - %s\n", $$1, $$2}'

init: ## install hook and dependencies
	@ln -sf $(CURDIR)/.hooks/pre-commit.sh .git/hooks/pre-commit
	@uv sync

clean: ## clean build artifacts
	@rm -rf build/ dist/ *.egg-info/ .venv/ .mypy_cache/ .ruff_cache/

update: ## update dependencies
	@uv lock --upgrade
	@uv sync

format: ## format the codebase
	@find src -type f -name '*.sh' -print0 | xargs -0 -r uv run shfmt --write --indent 4 --case-indent
	@uv run ruff format --force-exclude -- src

lint: ## lint the codebase
	@find src -type f -name '*.sh' -print0 | xargs -0 -r uv run shellcheck --external-sources --exclude=SC2034
	@uv run ruff check --quiet --force-exclude -- src
	@uv run mypy --pretty -- src

version: ## print application verison
	@uv run audiohook version
