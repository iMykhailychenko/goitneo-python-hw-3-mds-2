lint: 
	python -m isort **/*.py && python -m black **/*.py
test:
	python -m unittest discover app