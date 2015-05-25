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
    if not question:
        return None
    return question.flatten()


@main.route('/')
@main.route('/<qid>/')
def get_challenge(qid=None):
    question = None
    referral_choices = [(i, q['prompt']) for i, q in enumerate(QUESTIONS)]
    if qid and qid.isdigit():
        if int(qid) >= len(QUESTIONS):
            question = get_question(qid)
            referral_choices.insert(0, (qid, question['prompt']))
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
                           referral_choices=referral_choices,
                           og_title=og_title,
                           request=request)


@main.route('/<qid>/create_challenge', methods=['POST'])
@main.route('/create_challenge', methods=['POST'])
def create(qid=0):
    params = request.json
    name = params.get('name') or 'anonymous'
    prompt = params.get('prompt')
    correct_names = params.get('correct_names') or []
    passing_score = params.get('passing_score') or len(correct_names)
    question_id = r.get_registry()['QUESTIONS'].store(
        cgi.escape(name),
        cgi.escape(prompt),
        passing_score,
        [cgi.escape(n) for n in correct_names],
    )
    return jsonify({
        'question_id': question_id
    })
