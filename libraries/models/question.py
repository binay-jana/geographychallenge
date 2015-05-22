# -*- coding: utf-8; -*-
import ujson


class Question(object):
    def __init__(self, redis_data):
        for key, val in redis_data.iteritems():
            setattr(self, key, val)

    def flatten(self):
        correct_names = ujson.loads(self.correct_names)
        return {
            'total_answers': len(correct_names),
            'is_name_things': self.is_name_things,
            'prompt': self.prompt,
            'passing_score': self.passing_score,
            'answers': {v: i for i, v in enumerate(correct_names)},
            'names': correct_names
        }
