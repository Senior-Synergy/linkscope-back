# linkscope-back

## Initialization (first time)
1. Ensure that the current python version is >=3.7 and <=3.11
2. Create new python environment: `python -m venv .venv` or Mac OS, use: `python3 -m venv .venv`
3. Activate the environment : `.venv\Scripts\activate` for Mac OS, use: `source .venv/bin/activate`
4. Install all packages in requirement : `pip install -r requirements.txt`
4. To start the server : `uvicorn app.main:app --reload`

## Running the Sever Locally
1. Activate python environment : `.venv\Scripts\activate`
2. Check for requirement updates : `pip install -r requirements.txt`
3. Start the server : `uvicorn app.main:app --reload`

## Updating Requirements
Write requirement file and update :  `pip freeze > requirements.txt`