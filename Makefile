.PHONY: all test run lint clean

PYTHON = python3
PIP = pip3

all: test

clean:
	rm -rf packages
	rm -rfv target
	rm -rf **/__pycache__

packages/installed: requirements.txt requirements-dev.txt
	$(PIP) install -r requirements-dev.txt --target=./packages --upgrade
	touch packages/installed

lint: packages/installed
	PYTHONPATH=packages:src $(PYTHON) -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics --ignore=W191
	PYTHONPATH=packages:src $(PYTHON) -m flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --ignore=W191,E128
	PYTHONPATH=packages:src $(PYTHON) -m mypy src/

test: packages/installed lint
	PYTHONPATH=packages:src $(PYTHON) -m pytest

run: test
	PYTHONPATH=packages:src $(PYTHON) src/addon_updater.py -v -p "/Applications/World of Warcraft/_retail_/" "./_retail_"  --curseforge 957044 --github opussf/Calc
