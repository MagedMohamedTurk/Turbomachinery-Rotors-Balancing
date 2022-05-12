all: cd_project build install cd_test run_test

cd_project:
	cd ~/Turbomachinery-Rotors-Balancing/
build:
	python3 -m build
install:
	pip install -e .
cd_test:
	cd ~/Turbomachinery-Rotors-Balancing/test/
run_test:
	pytest -v
