.PHONY: test rmpyc

test:
	pytest tests/ --tb=short -v
	$(MAKE) rmpyc

rmpyc:
	find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +
