# TODO: optimization required...
from datetime import timedelta

from django.db import models
from django.db.models import Count
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import SerializerMethodField, FloatField, ModelSerializer, Serializer
from rest_polymorphic.serializers import PolymorphicSerializer

from commons.serializers import DynamicFieldsModelSerializer
from surveys.models import Question, Answer, ChoiceQuestion, MultiChoiceQuestion, InputQuestion, InputChoiceQuestion, \
    InputMultiChoiceQuestion, Survey, UserInputAnswer, UserAnswer, UserChoiceAnswer, UserMultiChoiceAnswer, \
    UserInputChoiceAnswer, UserInputMultiChoiceAnswer


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        exclude = ['content_type', 'object_id']


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        exclude = ['polymorphic_ctype']
        read_only_fields = ['survey']


class ChoiceQuestionSerializerMixin(Serializer):
    answers = AnswerSerializer(many=True)


class InputQuestionSerializer(ModelSerializer):
    class Meta(QuestionSerializer.Meta):
        model = InputQuestion


class ChoiceQuestionSerializer(ChoiceQuestionSerializerMixin, ModelSerializer):
    class Meta(QuestionSerializer.Meta):
        model = ChoiceQuestion


class MultiChoiceQuestionSerializer(ChoiceQuestionSerializerMixin, ModelSerializer):
    class Meta(QuestionSerializer.Meta):
        model = MultiChoiceQuestion


class InputChoiceQuestionSerializer(ChoiceQuestionSerializerMixin, ModelSerializer):
    class Meta(QuestionSerializer.Meta):
        model = InputChoiceQuestion


class InputMultiChoiceQuestionSerializer(ChoiceQuestionSerializerMixin, ModelSerializer):
    class Meta(QuestionSerializer.Meta):
        model = InputMultiChoiceQuestion


class QuestionPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'question_type'
    base_serializer_class = QuestionSerializer
    model_serializer_mapping = {
        InputQuestion: InputQuestionSerializer,
        ChoiceQuestion: ChoiceQuestionSerializer,
        MultiChoiceQuestion: MultiChoiceQuestionSerializer,
        InputChoiceQuestion: InputChoiceQuestionSerializer,
        InputMultiChoiceQuestion: InputMultiChoiceQuestionSerializer,
    }


class SurveySerializer(DynamicFieldsModelSerializer):
    questions = QuestionPolymorphicSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'

    def validate(self, attrs):
        # In partial update you don't need to pass all data, you can omit something.
        # And if `start_at` or `end_at` will be omitted, `.clean()` will set those fields to None,
        # and since you cannot compare None and None, so this code
        #
        # >>> if self.end_at > self.start_at: ...
        #
        # will raise an error.
        if getattr(self.context.get('view'), 'action', None) == 'partial_update':
            attrs.setdefault('start_at', timezone.now())
            attrs.setdefault('end_at', timezone.now() + timedelta(days=1))

        # Since serializers do not call `.full_clean()` method on models instances,
        # but in this case it is needed, workaround is used here.
        # https://www.django-rest-framework.org/community/3.0-announcement/#differences-between-modelserializer-validation-and-modelform
        fake = Survey(**attrs)
        fake.clean()
        return attrs


class AnswerResultsSerializer(ModelSerializer):
    pick_rate = FloatField()

    class Meta:
        model = Answer
        fields = ['id', 'text', 'pick_rate']


class InputAnswersMixin(Serializer):
    input_answers = SerializerMethodField()

    def get_input_answers(self, obj: Question):
        return list(obj.user_answers.filter(text__isnull=False).values_list('text', flat=True))


class SelectedAnswersMixin(Serializer):
    answers_user_answers_field: str = None
    selected_answers = SerializerMethodField()

    def get_selected_answers(self, obj: Question):
        if self.answers_user_answers_field is None:
            return None

        answers = obj.answers.annotate(pick_rate=Cast(
            Count(self.answers_user_answers_field) / float(obj.user_answers.count() or 1), models.FloatField()
        ))
        return AnswerResultsSerializer(answers, many=True).data


class InputQuestionResultsSerializer(InputAnswersMixin, QuestionSerializer):
    ...


class ChoiceQuestionResultsSerializer(SelectedAnswersMixin, QuestionSerializer):
    answers_user_answers_field = 'user_choices'


class MultiChoiceQuestionResultsSerializer(SelectedAnswersMixin, QuestionSerializer):
    answers_user_answers_field = 'user_multi_choices'


class InputChoiceQuestionResultsSerializer(InputAnswersMixin, SelectedAnswersMixin, QuestionSerializer):
    answers_user_answers_field = 'user_input_choices'


class InputMultiChoiceQuestionResultsSerializer(InputAnswersMixin, SelectedAnswersMixin, QuestionSerializer):
    answers_user_answers_field = 'user_input_multi_choices'


class QuestionResultsPolymorphicSerializer(QuestionPolymorphicSerializer):
    model_serializer_mapping = {
        InputQuestion: InputQuestionResultsSerializer,
        ChoiceQuestion: ChoiceQuestionResultsSerializer,
        MultiChoiceQuestion: MultiChoiceQuestionResultsSerializer,
        InputChoiceQuestion: InputChoiceQuestionResultsSerializer,
        InputMultiChoiceQuestion: InputMultiChoiceQuestionResultsSerializer,
    }


class SurveyResultsSerializer(DynamicFieldsModelSerializer):
    questions = QuestionResultsPolymorphicSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'


class UserAnswerSerializer(ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
        read_only_fields = ['question']


class UserChoiceAnswerValidationMixin(Serializer):
    def validate_answer(self, answer):
        question_pk = self.context['view'].kwargs['question_pk']
        question = Question.objects.get(pk=question_pk)

        if answer not in question.answers.all():
            raise ValidationError("Вашего варианта ответа нет в списке допустимых")

        return answer


class UserMultiChoiceAnswerValidationMixin(Serializer):
    def validate_answers(self, answers):
        question_pk = self.context['view'].kwargs['question_pk']
        question = Question.objects.get(pk=question_pk)
        allowed_answers = question.answers.all()

        if [a for a in answers if a not in allowed_answers]:
            raise ValidationError("Вашего варианта ответа нет в списке допустимых")

        return answers


class UserInputAnswerSerializer(ModelSerializer):
    class Meta(UserAnswerSerializer.Meta):
        model = UserInputAnswer


class UserChoiceAnswerSerializer(UserChoiceAnswerValidationMixin, ModelSerializer):
    class Meta(UserAnswerSerializer.Meta):
        model = UserChoiceAnswer


class UserMultiChoiceAnswerSerializer(UserMultiChoiceAnswerValidationMixin, ModelSerializer):
    class Meta(UserAnswerSerializer.Meta):
        model = UserMultiChoiceAnswer

    def validate(self, attrs):
        if not len(attrs['answers']) >= 1:
            raise ValidationError("Необходим как минимум один ответ")

        return super().validate(attrs)


class UserInputChoiceAnswerSerializer(UserChoiceAnswerValidationMixin, ModelSerializer):
    class Meta(UserAnswerSerializer.Meta):
        model = UserInputChoiceAnswer

    def validate(self, attrs):
        class MockAnswer:
            text = None

        if bool(attrs.get('answer', MockAnswer()).text) is bool(attrs.get('text', None)):
            raise ValidationError("Необходимо выбрать один из предложенных вариантов ответа, либо написать свой")

        return super().validate(attrs)


class UserInputMultiChoiceAnswerSerializer(UserMultiChoiceAnswerValidationMixin, ModelSerializer):
    class Meta(UserAnswerSerializer.Meta):
        model = UserInputMultiChoiceAnswer

    def validate(self, attrs):
        if (not len(attrs['answers']) >= 1) and (attrs['text'] is None):
            raise ValidationError("Необходим как минимум один ответ")

        return super().validate(attrs)


class UserAnswerPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'user_answer_type'
    base_serializer_class = UserAnswerSerializer
    model_serializer_mapping = {
        UserInputAnswer: UserInputAnswerSerializer,
        UserChoiceAnswer: UserChoiceAnswerSerializer,
        UserMultiChoiceAnswer: UserMultiChoiceAnswerSerializer,
        UserInputChoiceAnswer: UserInputChoiceAnswerSerializer,
        UserInputMultiChoiceAnswer: UserInputMultiChoiceAnswerSerializer,
    }
