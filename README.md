# Full Stack API Final Project

## Full Stack Trivia

Trivia app is a web application to manage the and play the trivia game. 

The application capabilities:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Getting Started

### Installing Dependencies

#### Frontend Dependencies

This project depends on Nodejs and Node Package Manager (NPM). So, download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. so, to install frontend dependecies open your terminal, naviging to the `/frontend` directory and run:

```bash
npm install
```

#### Backend Dependencies

##### Python 3.7.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
>_tip_: **Windows users need to install Microsoft Build Tools C++ 14.0 before installing PIP Dependencies and it can be downloaded and installed from [http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe.](http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe.)**

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Running server in development mode

#### Run Frontend 

After installing frontend dependencies, To run frontend in development mode run:

```bash
npm start
```

#### Run Backend 

After installing backend dependencies, To run backend in development mode run:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
>_tip_: **Windows users replace export keyword with set**

### Testing
To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started

- Base URL: The backend is hosted at http://127.0.0.1:5000/ and The frontend is hosted at http://127.0.0.1:3000/
- Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:

```bash
{
    'success': False,
    'error': 404,
    'message': 'resource not found'
}), 404
```

The API will return four types of errors:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error

### Resource endpoint Library

#### 1.GET /categories

- General: 

    - returns a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.

- Sample: 

    - curl http://127.0.0.1:5000/categories
    
    ```
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}
    ```
    
#### 2.GET /questions

- General: 

    - returns all questions from data base in pages and each page contains 10 questions.
    - Specific page can be requested by sending page variable within the URl.

- Sample: 

    - curl http://127.0.0.1:5000/questions
    
    ```
    {
      "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      },
      "questions": [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
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
        }
      ],
      "success": true,
      "total_questions": 19
    }
    ```

#### 3.POST /questions

- General: 

    - This endpoint used to do both create a new question and return a search result.
    - If the request doesn't contain searchTerm, the endpoint will post a new question.
    - If the request contains searchTerm, the endpoint will return a search result for requested searchTerm.

- Sample: 

    - To post new question: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Which trophy have Al Ahly egyptian team won in FIFA club world cup 2020 ?", "answer": "Bronze Medal", "difficulty": 2, "category": "6" }'
    
    ```
    {
      "created": 25,
      "questions": [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
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
        }
      ],
      "success": true,
      "total_questions": 20
    }
    ```
    
    - To search for a term 'won': curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "won"}'
    
    ```
    {
      "questions": [
        {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
          "answer": "Bronze Medal",
          "category": 6,
          "difficulty": 2,
          "id": 25,
          "question": "Which trophy have Al Ahly egyptian team won in FIFA club world cup 2020?"
        }
      ],
      "success": true,
      "total_questions": 20
    }
    ```

#### 4.DELETE /questions/<int:question_id>

- General: 

    - This endpoint delets a question using question_id.

- Sample: 

    - curl http://127.0.0.1:5000/questions/25 -X DELETE
    
    ```
    {
      "message": "Question deleted successfully",
      "success": true
    }
    ```

#### 5.GET /categories/<int:category_id>/questions

- General: 

    - This endpoint returns all questions of the requested category using category_id.

- Sample: 

    - curl http://127.0.0.1:5000/categories/1/questions
    
    ```
    {
      "current_category": "Science",
      "questions": [
        {
          "answer": "The Liver",
          "category": 1,
          "difficulty": 4,
          "id": 20,
          "question": "What is the heaviest organ in the human body?"
        },
        {
          "answer": "Alexander Fleming",
          "category": 1,
          "difficulty": 3,
          "id": 21,
          "question": "Who discovered penicillin?"
        },
        {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        }
      ],
      "success": true,
      "total_questions": 3
    }
    ```

#### 6.POST /quizzes

- General: 

    - This endpoint for starting the game and it returns random question each time from the quiz category.

- Sample: 

    - curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 11, 15], "quiz_category": { "id": 0}}'
    
    ```
    {
      "question": {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      "success": true
    }
    ```
    
## Authors

Peter Ayad halped to author the backend endpoints in flaskr app to integrate with the frontend which authored by the awsome team of Udacity.
