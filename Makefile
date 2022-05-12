all: cd_project build install cd_test run_test

<<<<<<< HEAD
test: cd_test run_test

=======
>>>>>>> 5f47d44a7378c49122ccea8127e3f91d4237a771
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
