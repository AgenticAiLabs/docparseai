.PHONY: install test rmpyc

test:
	$(MAKE) install
	pytest tests/ --tb=short -v
	$(MAKE) rmpyc

rmpyc:
	find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +

install:
	pip install -e .

deploy:
	rm -rf dist/ build/ *.egg-info
	python -m build
	twine upload dist/*