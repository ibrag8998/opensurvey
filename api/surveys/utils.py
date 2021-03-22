from typing import Union, Type

from django.apps import apps
from django.db import models
from django.db.models import Model


class QuestionAnswerMapping:
    QUESTION_ANSWER = {
        'inputquestion': 'userinputanswer',
        'choicequestion': 'userchoiceanswer',
        'multichoicequestion': 'usermultichoiceanswer',
        'inputchoicequestion': 'userinputchoiceanswer',
        'inputmultichoicequestion': 'userinputmultichoiceanswer',
    }

    ANSWER_QUESTION = {
        'userinputanswer': 'inputquestion',
        'userchoiceanswer': 'choicequestion',
        'usermultichoiceanswer': 'multichoicequestion',
        'userinputchoiceanswer': 'inputchoicequestion',
        'userinputmultichoiceanswer': 'inputmultichoicequestion',
    }

    def _get_mapping_value(self, key, mapping):
        if isinstance(key, models.Model):
            key = key._meta.object_name
        elif isinstance(key, type):
            key = key.__name__

        return apps.get_model('surveys', mapping[key.lower()])

    def get_answer_model(self, question: Union[str, Model, Type[Model]]) -> Type[Model]:
        return self._get_mapping_value(question, self.QUESTION_ANSWER)

    def get_question_model(self, answer: Union[str, Model, Type[Model]]) -> Type[Model]:
        return self._get_mapping_value(answer, self.ANSWER_QUESTION)


qa_mapping = QuestionAnswerMapping()
