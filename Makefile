test:
	py.test tests

clean:
	rm -rf **/*.pyc **/__pycache__

deps:
	pip install .
