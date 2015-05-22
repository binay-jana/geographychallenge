import ujson
import registry as r
from libraries.models.question import Question


class Questions(object):
    TAG = "questions"

    @classmethod
    def get_redis_key(cls, key):
        return cls.TAG + ':' + str(key)

    @classmethod
    def get(cls, id):
        redis_key = cls.get_redis_key(id)
        cached_data = r.get_registry()['REDIS'].hgetall(redis_key)
        if cached_data:
            return Question(cached_data)
        query = "SELECT * FROM questions WHERE id=%s"
        result = r.get_registry()['MY_SQL'].get(query, [id])
        if result:
            cls.cache_result(result)
            return Question(result)
        return None

    @classmethod
    def cache_result(cls, question):
        r.get_registry()['REDIS'].hmset(
            cls.get_redis_key(question['id']), question
        )

    @classmethod
    def store(cls, is_name_things, title, prompt, passing_score,
              correct_names, question_answer_set):
        query = """INSERT INTO questions(is_name_things, prompt,
            passing_score, correct_names, question_answer_set)
         VALUES (
            %(is_name_things)s,
            %(prompt)s,
            %(passing_score)s,
            %(correct_names)s,
            %(question_answer_set)s
        );"""
        row_id = r.get_registry()['MY_SQL'].insert(
            query,
            {
                'is_name_things': 1 if is_name_things else 0,
                'prompt': prompt,
                'passing_score': passing_score,
                'correct_names': ujson.dumps(correct_names),
                'question_answer_set': ujson.dumps(question_answer_set)
            }
        )
        return row_id
