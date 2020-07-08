import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={'/api': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        # Access Control Allow for Headers and Methods
        response.headers.add('Access-Control-Headers',
                             'Content-Type,Authorization,True')
        response.headers.add('Access-Control-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Create an endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        category_list = {
            category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': category_list,
            'status':200 #success
        })

    # Create an endpoint to handle GET requests for questions, including pagination (every 10 questions).

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():

        selection = Question.query.order_by(Question.id).all()
        current_query = paginate_questions(request, selection)

        # Use above categories and paste them here
        # list categories

        categories = Category.query.all()
        category_list = {category.id: category.type for category in categories}
        categories = list(map(Category.format, Category.query.all()))

        # abort 404 if current questions is none
        if len(current_query) == 0:
            abort(404)

        # return jsonify if success
        return jsonify({
            'success': True,
            'questions': current_query,
            'total_questions': len(Question.query.all()),
            'categories': category_list,
            'current_category': None

        })

    # Create an endpoint to DELETE question using a question ID.

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleted_questions(question_id):

        try:
      
            deleted_questions = Question.query.filter(
                Question.id == question_id).one_or_none()

            # abort 404 if deleted questions is none
            if deleted_questions is None:
                abort(404)

            # delete questions
            deleted_questions.delete()
            selection = Question.query.order_by(Question.id).all()
            current_query = paginate_questions(request, selection)

            # return jsonify if success
            return jsonify({
                'success': True,
                'deleted_questions_id': question_id,
                'questions': current_query,
                'total_questions': len(Question.query.all())
            })

        except Exception as e:
            print(e)
            abort(422)

    # Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        new_question = data.get('question',None)
        new_answer   =  data.get('answer',None)
        new_difficulty = data.get('difficulty',None)
        new_category   = data.get('category',None)

        try:
            # get new information
            question = Question(question = new_question, answer = new_answer,difficulty = new_difficulty,category = new_category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()


            # return jsonify if success
            return jsonify({
                'success': True,
                'created': question.id,
                'total_questions': len(selection)
            })
        except Exception as e: 
            print(e)
            abort(422)

    # Create a POST to search new questions
    @app.route('/questions/search', methods=['POST'])
    def search_new_questions():

        # load quest for data
        data = request.get_json()
        # get new search term
        new_search = data.get('searchTerm', None)

        # get new  search results (if the udacity book search result doesnt work remove it from create question
        # and create a separate search result POST )
        if new_search:
            selection = Question.query.filter(
                Question.question.ilike(f'%{new_search}%')).all()
            question_query = paginate_questions(request, selection)

            # abort(404) if search term is None meaning in order to return the a response it must abort(404)
            if new_search is None:
                abort(404)

            # return jsonify if success
            return jsonify({
                'success': True,
                'questions': question_query,
                'total_questions': len(selection),
            })

    # GET endpoint to get questions based on category

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        try:
            # filter category id and question id
            selection = Question.query.filter(
                Question.category == category_id).order_by(Question.id).all()
            # paginated current question by using request and selection
            current_query = paginate_questions(request, selection)
            # return jsonify if success
            return jsonify({
                'success': True,
                'questions': current_query,
                'current_category': category_id,
                'total_questions': len(selection),
            })
        except Exception as e:
            print(e)
            abort(404)

    # Create an endpoint to POST to play quiz
    @app.route('/quizzes', methods=['POST'])
    def play_random_quiz():

        try:
            data = request.get_json()
            print(data)
    
            # get quiz category and previous questions(similar like POST create question)
            quiz_category = data.get('quiz_category', None)
            previous_qs = data.get('previous_questions', None)
            print(previous_qs)

            # print previous question and filter them into dictionary
            test_questions = Question.query.filter(
                Question.id.notin_(previous_qs)).all()
            # get category id and if category is 0 query them all
            if quiz_category['id'] == 0:
                test_questions = Question.query.all()
            else:
                # else filter both previous questions and quiz category
                Question.query.filter(Question.id.notin_(previous_qs),
                                      Question.category == quiz_category['id']).all()
            # return josnify if sucess
            return jsonify({
                'success': True,
                'question': random.choice(test_questions).format()
            })
        except Exception as e:
            print(e)
            abort(422)

    # Create error handlers for all expected errors including 404 and 422.
    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
