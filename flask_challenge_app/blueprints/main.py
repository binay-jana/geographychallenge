# -*- coding: utf-8; -*-
from flask import Blueprint, render_template
from libraries.Log import Log

main = Blueprint('main', __name__)

_logger = Log.getLogger(__name__)


@main.route('/')
def index():
    return render_template('trivia.html')

# @main.route('/create_challenge', methods=['POST'])
#     