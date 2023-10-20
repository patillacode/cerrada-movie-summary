install: ## Install the necessary dependencies
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

run: ## Run the summary script
	. venv/bin/activate
	python summary.py

clean: ## Clean up the generated files
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf sumarios
	rm -rf venv

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
