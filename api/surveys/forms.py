from django.forms import ModelForm, HiddenInput

from surveys.models import Question, ChoiceQuestion, InputQuestion, MultiChoiceQuestion, InputChoiceQuestion, \
    InputMultiChoiceQuestion


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'position': HiddenInput()
        }


class InputQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        model = InputQuestion


class ChoiceQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        model = ChoiceQuestion


class MultiChoiceQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        model = MultiChoiceQuestion


class InputChoiceQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        model = InputChoiceQuestion


class InputMultiChoiceQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        model = InputMultiChoiceQuestion
