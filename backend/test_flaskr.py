import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
      # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    #  Write tests for search - at minimum two that check a response when there are results and when there are none
    
    def test_deleted_questions(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_questions_id'], 10)      

    def test_already_deleted_question_fail(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_insert_question(self):
        new_question = {
            'question': 'Where is Chris Hadfield from?',
            'answer': 'Canada',
            'category':'1',
            'difficulty':'1'
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_insert_question_fail(self):
        new_question = {
            'question': 'Where is Chris Hadfield from?',
            'answer': 'Canada',
            'category':'1',
            'difficulty':'1'
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_search_question(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': "Who invented peanut butter?"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)     
    
    def test_422_post_quizzes(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__" :
    unittest.main()
