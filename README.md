# Mytheresa-api
Queryable REST api project

Requirements for the project:

Python 3.10.6 preferred though any fairly recent release should suffice

- create and activate virtual environment within project directory

- pip3 install -r requirements.txt

Run Project:

- python app.py 

Run Tests:

- pytest tests.py     --requires project to have been run at least once to populate db

Notes:

- I chose to use python since it's what I've been using more recently and Flask as the framework because it is lightweight enough and doesn't abstract my code away as much as django would.

- The endpoint to use is http://127.0.0.1:5000/product so long as the port specified in app.py is 5000


Limitations:

-Change in discount would require the user to post products again

-Large numbers of products would be slower as they take a transaction each (multiprocessing/batch transactions would fix this)

