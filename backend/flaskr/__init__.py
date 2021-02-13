import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def all_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories={}
    for category in categories:
        formatted_categories[category.id]= category.type
    
    if (len(formatted_categories) == 0):
        abort(404)
            
    return formatted_categories

def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]
    
    current_questions = formatted_questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
  
    #Set up CORS. Allow '*' for origins.
    CORS(app, resources={'/': {'origins': '*'}})

    #Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    #endpoint to handle GET requests for all available categories.
    @app.route('/categories')
    def get_categories():
        try:
            categories_list= all_categories()

            return jsonify({
                'success': True,
                'categories': categories_list
            }), 200
        except:
            abort(500)
        
    #endpoint to handle GET requests for questions, including pagination (every 10 questions). 
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)
        current_questions = paginate_questions(request, questions)

        categories_list= all_categories()

        if (len(current_questions) == 0):
            abort(404)
                
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_list
        }), 200

    #endpoint to DELETE question using a question ID. 
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id==question_id).one_or_none()
            
            if question is None:
                abort(404)
            
            question.delete()
            
            return jsonify({
                'success': True,
                'message': 'Question deleted successfully'
            }), 200
        except:
            abort(422)

    #endpoint to POST a new question or search in questions
    @app.route('/questions', methods=['POST'])
    def post_question():
        #this function to handle both create a new question and search in questions 
        body = request.get_json()
        
        #searching
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')
            result = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()
            
            if (len(result) == 0):
                abort(404)
            
            current_result = paginate_questions(request, result)
            total_questions = len(Question.query.all())
            
            return jsonify({
                'success': True,
                'questions': current_result,
                'total_questions': total_questions
            }), 200
        
        #creating new question
        else:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)
            
            if ((new_question is None) or (new_answer is None) or (new_difficulty is None) or (new_category is None)):
                abort(422)
            
            try:
                new_question_resource = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                new_question_resource.insert()
                
                questions = Question.query.order_by(Question.id).all()
                total_questions = len(questions)
                current_questions = paginate_questions(request, questions)
                
                return jsonify({
                    'success': True,
                    'created': new_question_resource.id,
                    'questions': current_questions,
                    'total_questions': total_questions
                }),201
            except:
                abort(422)
                                
    #endpoint to get questions based on category. 
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category = Category.query.filter(Category.id==category_id).one_or_none()
        
        if (category is None):
            abort(400)
            
        questions = Question.query.filter_by(category=category.id).all()
        total_questions = len(questions)
        current_questions = paginate_questions(request, questions)
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'current_category': category.type
        }),200

    #POST endpoint to get questions to play the quiz. 
    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')
        
        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)
            
        if (quiz_category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=quiz_category['id']).all()

        question_id_list=[question.id for question in questions]
        
        is_used=True
        
        while is_used:
            question_id=random.choice(question_id_list)
            if question_id in previous_questions:
                question_id=random.choice(question_id_list)
            else:
                is_used=False
            
        next_question=Question.query.filter_by(id=question_id).one_or_none()
        
        return jsonify({
            'success': True,
            'question': next_question.format(),
        }), 200
    
    #error handlers for all expected errors 
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400
    
    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

  
    return app
