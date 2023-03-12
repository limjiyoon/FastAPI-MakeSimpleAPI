setup:
	pdm venv create 3.10
	pdm use .venv/bin/python
	pdm install

run:
	uvicorn fastapi-makesimpleapi.main:app --reload
