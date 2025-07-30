.PHONY: help init clean test validate mock create delete info deploy
.DEFAULT_GOAL := help
environment = "inlined"

help:
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## clean
		-@pipenv --rm
		@find . -name "*.pyc" -exec rm -f {} \;
		@find . -name "__pycache__" -exec rm -rf {} \;
		@rm -rf .pytest_cache

run_local: ## run the ms in local environment (remember to export the AWS credentials on terminal before running this)
		@pipenv run python -m uvicorn src.applications.app_service:app --reload --host 0.0.0.0 --port 8000

install_local: ## install requirements in conda
	( \
		python -m pip install --no-cache-dir -r requirements-dev.txt
	)

test_local: ## run the unit test in conda env
	( \
		python -m pytest -x -vv --cov=src --cov-config=.coveragerc tests/unit-test; \
		python -m coverage xml; \
		python -m coverage html; \
	)

docker-build:
	docker build -f deployment/Dockerfile -t preprocessing_ms .

docker-start:
	docker run -d -p 8000:8000 --name preprocessing_ms preprocessing_ms




