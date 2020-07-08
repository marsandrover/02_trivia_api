# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Other installation requirements

Also make sure you have the following installed. So just incase if pip install -r requirements.txt doesnt install properly make sure you have flask,flask-cors and sqlalchemy installed and here is how to install them :

Installing the following extension with using pip, or easy_install:

```bash
pip install flask
```
```bash
pip install flask-cors
```
```bash
 pip install -U Flask-SQLAlchemy
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
or 
```bash
psql -d trivia -U postgres -a -f trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute (I am running on windows so its different if youre running it on linux or mac for more follow this tutorial: https://dev.to/sahilrajput/install-flask-and-create-your-first-web-application-2dba

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
python -m flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API References
### Getting Started
This Backend server is hosted at `http://127.0.0.1:5000/` since its only hosted locally.
User authentication : This version doesn't require any authenication or user key id.

## Error Handling
Errors are returned as json in the following format:


```bash
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```
The API will return three types of errors:

400: bad request
404: resource not found
422: unprocessable

## Endpoints
### GET/categories
- Returns a list of categories and success values
- Sample: `curl http://12.0.0.1:5000/categories`   

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
### GET/questions
- Returns list of questions and are paginated in groups of 10.(unix)
- It also returns lists of categories and total number of questions.(reussir)
- Sample: `curl http://12.0.0.1:5000/questions`
    
 ```bash
 {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current categories": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "success": true,
  "total_questions": 59
}
 ```
 
### DELETE/questions /<question_id>
- Deletes questions by using url parameters.
- When a question gets deleted it returns with id of deleted question upon success but 422 if unsucessful.
- Sample: curl  `curl http://12.0.0.1:5000/30 -X DELETE`

```bash
{
  "deleted": 30,
  "questions": 10,
  "success": true
}
```
### POST/questions
-  Post creates a new question using json when you insert new questions (nouvelle question)
- It returns id of created questions if success.(reussir)
- Sample: `curl http://12.0.0.1:5000/questions -X  POST -H "Content-Type: application/json" -d '{"questions": "Off what country are the islands of Islay, Mull, and St. Kilda located - Ireland, Scotland, or Iceland?"-d , "answer":"Scotland - There are over 790 islands in Scotland; around 130 are inhabited.","difficulty":3,"category":"3"} `

```bash
{
  "created": 73,
  "success": true,
  "total_questions": 62
}
```

### POST/questions/search

- If search term is included it will return with  id of questions if success (reussir)
- Sample: `curl http://12.0.0.1:5000/questions -X  POST -H "Content-Type: application/json" -d '{'searchTerm":Who invented peanut butter?"}'`

```bash
{
  "questions": [
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    }
  ],
  "success": true,
  "total_questions": 1
}
    
```

### GET/categories /<int:id>/questions

- Get questions based on category id  using url paramaters. 
- If success it returns json object with paginated matching questions.
- Sample `curl http://12.0.0.1:5000/categories/1/questions`

```bash

{
  "current_category": {
    "id": 1,
    "type": "Science"
  },
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "27%",
      "category": 1,
      "difficulty": 3,
      "id": 24,
      "question": "What percent of the universe is dark matter? "
    },
    {
      "answer": "Eight planets",
      "category": 1,
      "difficulty": 2,
      "id": 25,
      "question": "How many planets are in the Solar System? "
    },
    {
      "answer": "Jupiter",
      "category": 1,
      "difficulty": 1,
      "id": 26,
      "question": "What is the largest planet in our solar system? "
    },
    {
      "answer": "Mercury",
      "category": 1,
      "difficulty": 2,
      "id": 27,
      "question": "What is the smallest planet in our solar system? "
    },
    {
      "answer": "Baby",
      "category": 1,
      "difficulty": 2,
      "id": 28,
      "question": "Which of the following has more bones? "
    },
    {
      "answer": "Oxygen",
      "category": 1,
      "difficulty": 1,
      "id": 29,
      "question": "What is the most common element in the human body? "
    },
    {
      "answer": "Lungs",
      "category": 1,
      "difficulty": 2,
      "id": 30,
      "question": "Which organ do insects NOT have? "
    }
  ],
  "success": true,
  "total_questions": 8
}
```

### POST/quizzes

 - When you play it will return random questions using the submitted category and previous questions.
 - Sample: `curl http://12.0.0.1:5000/questions -X  POST -H "Content-Type: application/json" -d '{"previous_questions":[26,27],"quiz_category": {"type":"Science", "id":"1"}}`
    
```bash
    
{
  "question": {
    "answer": "Oxygen",
    "category": 1,
    "difficulty": 1,
    "id": 29,
    "question": "What is the most common element in the human body? "
  },
  "success": true
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
