# -*- coding: utf-8; -*-
from flask import Blueprint, render_template, request, jsonify
from libraries.Log import Log
import registry as r
import cgi
import ujson
from random import randint
from libraries.stock_questions import QUESTIONS

main = Blueprint('main', __name__)

_logger = Log.getLogger(__name__)


def get_random_stock_question_id():
    return randint(0, len(QUESTIONS) - 1)


def get_question(question_id):
    if not question_id:
        return None
    question = r.get_registry()['QUESTIONS'].get(question_id)
    return question.flatten()


@main.route('/')
@main.route('/<qid>/')
def get_challenge(qid=None):
    question = None
    if qid and qid.isdigit():
        if int(qid) >= len(QUESTIONS):
            question = get_question(qid)
        else:
            question = QUESTIONS[int(qid)]
    if not question:
        question = QUESTIONS[get_random_stock_question_id()]
    if qid is None:
        og_title = "for Nepal Earthquake Relief"
    else:
        og_title = ": " + question['prompt']
    return render_template('trivia.html',
                           question=ujson.dumps(question),
                           og_title=og_title,
                           request=request)


@main.route('/create_challenge', methods=['POST'])
def create():
    params = request.json
    is_name_things = params.get('is_name_things')
    prompt = params.get('prompt')
    correct_names = params.get('correct_names') or []
    passing_score = params.get('passing_score') or len(correct_names)
    question_answer_sets = params.get('question_answer_sets') or []
    question_id = r.get_registry()['QUESTIONS'].store(
        is_name_things,
        cgi.escape(prompt),
        passing_score,
        correct_names,
        question_answer_sets
    )
    return jsonify({
        'question_id': question_id
    })
