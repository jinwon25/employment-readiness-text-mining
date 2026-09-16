PYTHON ?= python

.PHONY: assets notebook test validate check

assets:
	$(PYTHON) scripts/build_portfolio_assets.py

notebook:
	$(PYTHON) scripts/build_summary_notebook.py
	jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=120 notebooks/portfolio_summary.ipynb

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

validate:
	$(PYTHON) scripts/validate_repository.py

check: assets notebook test validate
