from django.test import TestCase

from surveys.models import InputQuestion, UserInputAnswer, ChoiceQuestion, UserChoiceAnswer, MultiChoiceQuestion, \
    UserMultiChoiceAnswer, InputChoiceQuestion, UserInputChoiceAnswer, InputMultiChoiceQuestion, \
    UserInputMultiChoiceAnswer
from surveys.utils import qa_mapping


class QAMappingTest(TestCase):
    fixtures = ['surveys']

    def test_input_question(self):
        self.assertTrue(
            qa_mapping.get_answer_model(
                InputQuestion
            ) is qa_mapping.get_answer_model(
                'inputquestion'
            ) is qa_mapping.get_answer_model(
                InputQuestion.objects.first()
            ) is UserInputAnswer
        )

    def test_choice_question(self):
        self.assertTrue(
            qa_mapping.get_answer_model(
                ChoiceQuestion
            ) is qa_mapping.get_answer_model(
                'choicequestion'
            ) is qa_mapping.get_answer_model(
                ChoiceQuestion.objects.first()
            ) is UserChoiceAnswer
        )

    def test_multi_choice_question(self):
        self.assertTrue(
            qa_mapping.get_answer_model(
                MultiChoiceQuestion
            ) is qa_mapping.get_answer_model(
                'multichoicequestion'
            ) is qa_mapping.get_answer_model(
                MultiChoiceQuestion.objects.first()
            ) is UserMultiChoiceAnswer
        )

    def test_input_choice_question(self):
        self.assertTrue(
            qa_mapping.get_answer_model(
                InputChoiceQuestion
            ) is qa_mapping.get_answer_model(
                'inputchoicequestion'
            ) is qa_mapping.get_answer_model(
                InputChoiceQuestion.objects.first()
            ) is UserInputChoiceAnswer
        )

    def test_input_multi_choice_question(self):
        self.assertTrue(
            qa_mapping.get_answer_model(
                InputMultiChoiceQuestion
            ) is qa_mapping.get_answer_model(
                'inputmultichoicequestion'
            ) is qa_mapping.get_answer_model(
                InputMultiChoiceQuestion.objects.first()
            ) is UserInputMultiChoiceAnswer
        )
