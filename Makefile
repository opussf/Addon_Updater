.PHONY: all test lint clean

PYTHON = python3
PIP = pip3

all: test

clean:
	rm -rf packages
	rm -f packages-dev-installed

.packages-dev-installed: requirements.txt requirements-dev.txt
	$(PIP) install -r requirements-dev.txt --target=./packages
	touch packages-dev-installed

lint: .packages-dev-installed
	PYTHONPATH=packages:src $(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --ignore=W191
	PYTHONPATH=packages:src $(PYTHON) -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --ignore=W191,E128

test: .packages-dev-installed lint
	PYTHONPATH=packages:src $(PYTHON) -m pytest --cov=pybattlenet --cov-report=xml:cobertura.xml --cov-report=html  --cov-report=term-missing -v
