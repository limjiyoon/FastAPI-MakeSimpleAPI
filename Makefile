setup:
	pdm venv create 3.10
	pdm use .venv/bin/python
	pdm install

run:
	uvicorn fastapi_makesimpleapi.main:app --reload

utest:
	pytest -v tests
