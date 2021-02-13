import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'admin' ,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        #question to be used in testing
        self.new_question={
            'question': 'Which trophy have Al Ahly egyptian team won in FIFA club world cup 2020 ?',
            'answer': 'Bronze Medal',
            'difficulty': 2,
            'category': '6'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    #test get categories successfully
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    #test get questions successfully
    def test_get_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    #test get invaled questions page
    def test_404_not_found_get_questions(self):
        res=self.client().get('/questions?page=10000')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    #test create question successfully
    def test_post_questions(self):
        res=self.client().post('/questions', json=self.new_question)
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['created'])
        
    #test failure of question creation
    def test_422_unprocessable_post_questions(self):
        res=self.client().post('/questions', json={})
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    #test delete question successfully
    def test_delete_questions(self):
        new_question = Question.query.order_by(self.db.desc(Question.id)).first()
        new_question_id = new_question.id
        res=self.client().delete('/questions/{}'.format(new_question_id))
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question deleted successfully')
        
    #test failure of question deletion
    def test_404__not_found_delete_questions(self):
        res=self.client().delete('/questions/100000')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    #test search questions successfully
    def test_search_questions(self):
        res=self.client().post('/questions', json={'searchTerm': 'won'})
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
    
    #test failure search questions
    def test_404_not_found_search_questions(self):
        res=self.client().post('/questions', json={'searchTerm': 'asdwrfse'})
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    #test get questions by category successfully
    def test_get_questions_by_category(self):
        res=self.client().get('/categories/1/questions')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    #test failure get questions by category
    def test_400_bad_request_get_questions_by_category(self):
        res=self.client().get('/categories/1000/questions')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        
    #test get quiz question successfully
    def test_post_quiz_question(self):
        res=self.client().post('/quizzes', json={
            'previous_questions':[2, 11, 15],
            'quiz_category': {'id':0}
        })
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    #test failure get quiz question
    def test_400_bad_request_post_quiz_question(self):
        res=self.client().post('/quizzes', json={
            'previous_questions':[2, 11, 15]
        })
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()