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
		@pipenv run python -m uvicorn src.applications.app_service:app --reload --host 0.0.0.0 --port 8001

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

local-stack: ## run the local stack

		-@aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name local-aio-r2-dev-sqs-reception-queue.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true

		-@aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket local-aid-r2-dev-s3-bucket

		-@aws --endpoint-url=http://localhost:4566 sns create-topic --name local-aid-r2-dev-sns-generic-error

docker-build:
	docker build -f deployment/Dockerfile -t improve_question_ms .

docker-start:
	docker run -d -p 8001:8001 --name improve_question_ms improve_question_ms




