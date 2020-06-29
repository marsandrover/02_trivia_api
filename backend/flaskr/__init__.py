import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={'/': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Create an endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.all()
        categories_formatted = {
            category.id: category.type for category in categories}

        if categories_formatted == {}:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_formatted
        })
    # Create an endpoint to handle GET requests for questions, including pagination (every 10 questions).

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        formatted_category = {
            category.id: category.type for category in categories}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': formatted_category,
            'total_questions': len(Question.query.all()),
            'current categories': None

        })
    # Create an endpoint to DELETE question using a question ID.

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            # delete the questions
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': len(current_questions),
            })
        except:
            abort(422)
    # Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.

    @app.route('/questions', methods=['POST'])
    def add_or_create_questions():

        # get request for body from json
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('diffculty')

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            # return jsonify if success
            return jsonify({
                'success': True,
                'created': question.id,

            })
        except:
            abort(422)
    # Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.

    @app.route('/questions/search', methods=['POST'])
    def search_new_question():
        search_term = request.get_json()['searchTerm']
        data = Question.query.filter(
            Question.question.ilike(f'%{search_term}%'))
        result = [question.format() for question in data]

        # return to jsonify if success
        return jsonify({
            'success': True,
            'questions': result,
            'total_questions': len(Question.query.all())
        })
    # Create a GET endpoint to get questions based on category.

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        try:
            selected_category = Category.query.get(category_id)
            questions = Question.query.filter(
                Question.category == category_id).order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': selected_category.format(),
                'total_questions': len(questions)
            })
        except:
            abort(404)

    # Create a POST endpoint to get questions to play the quiz.
    @app.route('/quizzes', methods=['POST'])
    def play_random_quiz():

        try:
            # get request for body
            body = request.get_json()

            # abort 422 if quiz category and previous questions not in body
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)

            # get category request
            category = body.get('quiz_category')
            # get previous questions request
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                # get available questions filtered by category id and question id
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(Question.id.notin_((previous_questions))).all()
            # see if new questions are avaiable
            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None

            # return jsonify results if success
            return jsonify({
                'success': True,
                'question': new_question

            })
        except:
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
