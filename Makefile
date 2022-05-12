all: build install cd_test run_test

test: cd_test run_test

build:
	python3 -m build
install:
	pip install -e .
cd_test:
	cd ./test/
run_test:
	pytest -v
