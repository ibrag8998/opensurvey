from html import unescape

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator
from polymorphic.models import PolymorphicModel

from commons.models import NON_POLYMORPHIC_CASCADE


class Survey(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    description = RichTextUploadingField('описание')
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    start_at = models.DateTimeField("дата начала")
    end_at = models.DateTimeField("дата окончания")

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def clean(self):
        """
        `.end_at` must be later then `.start_at`. This is crucial.
        """
        if not self.end_at > self.start_at:
            raise ValidationError("Опрос не может закончиться до того, как начнется")

    def get_status_display(self):
        if not self.is_started():
            return 'ожидает'
        if self.is_ended():
            return 'завершен'
        return 'активен'

    def is_started(self):
        return timezone.now() > self.start_at

    def is_ended(self):
        return timezone.now() > self.end_at


class Answer(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey()

    text = RichTextUploadingField('текст ответа')

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
        ordering = ['-id']

    def __str__(self):
        return strip_tags(unescape(Truncator(self.text).words(20, html=True, truncate=' …')))


# Questions

class Question(PolymorphicModel):
    survey = models.ForeignKey(Survey, on_delete=NON_POLYMORPHIC_CASCADE, related_name='questions',
                               verbose_name='опрос')

    text = RichTextUploadingField('текст вопроса')
    position = models.PositiveSmallIntegerField('позиция', default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return strip_tags(unescape(Truncator(self.text).words(20, html=True, truncate=' …')))


class BaseChoiceQuestion(Question):
    answers = GenericRelation(Answer)

    class Meta(Question.Meta):
        abstract = True


class InputQuestion(Question):
    class Meta(Question.Meta):
        verbose_name = 'вопрос с пользовательским вводом'
        verbose_name_plural = 'вопросы с пользовательским вводом'


class ChoiceQuestion(BaseChoiceQuestion):
    class Meta(Question.Meta):
        verbose_name = 'вопрос с одиночным выбором'
        verbose_name_plural = 'вопросы с одиночным выбором'


class MultiChoiceQuestion(BaseChoiceQuestion):
    class Meta(Question.Meta):
        verbose_name = 'вопрос с множественным выбором'
        verbose_name_plural = 'вопросы с множественным выбором'


class InputChoiceQuestion(BaseChoiceQuestion):
    class Meta(Question.Meta):
        verbose_name = 'вопрос с одиночным выбором и пользовательским вводом'
        verbose_name_plural = 'вопросы с одиночным выбором и пользовательским вводом'


class InputMultiChoiceQuestion(BaseChoiceQuestion):
    class Meta(Question.Meta):
        verbose_name = 'вопрос с множественным выбором и пользовательским вводом'
        verbose_name_plural = 'вопросы с множественным выбором и пользовательским вводом'


# User answers

class UserAnswer(PolymorphicModel):
    question: models.ForeignKey

    class Meta:
        verbose_name = "ответ пользователя"
        verbose_name_plural = "ответы пользователя"
        ordering = ['-id']


class UserInputAnswer(UserAnswer):
    question = models.ForeignKey(InputQuestion, on_delete=models.CASCADE, related_name='user_answers',
                                 verbose_name="вопрос")

    text = models.TextField("текст")

    def __str__(self):
        return self.text


class UserChoiceAnswer(UserAnswer):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name='user_answers',
                                 verbose_name="вопрос")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='user_choices', verbose_name="ответ")

    def __str__(self):
        return self.answer.text


class UserMultiChoiceAnswer(UserAnswer):
    question = models.ForeignKey(MultiChoiceQuestion, on_delete=models.CASCADE, related_name='user_answers',
                                 verbose_name="вопрос")
    answers = models.ManyToManyField(Answer, related_name='user_multi_choices', verbose_name="ответы")

    def __str__(self):
        if not self.pk:
            return '-'
        return ', '.join(self.answers.values_list('text', flat=True))


class UserInputChoiceAnswer(UserAnswer):
    question = models.ForeignKey(InputChoiceQuestion, on_delete=models.CASCADE, related_name='user_answers',
                                 verbose_name="вопрос")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='user_input_choices',
                               verbose_name="ответ", blank=True, null=True)

    text = models.TextField("текст", blank=True, null=True)

    def __str__(self):
        try:
            return self.answer.text
        except AttributeError:
            return f"other: {self.text}"


class UserInputMultiChoiceAnswer(UserAnswer):
    question = models.ForeignKey(InputMultiChoiceQuestion, on_delete=models.CASCADE, related_name='user_answers',
                                 verbose_name="вопрос")
    answers = models.ManyToManyField(Answer, related_name='user_input_multi_choices', verbose_name="ответы")

    text = models.TextField("текст", blank=True, null=True)

    def __str__(self):
        if not self.pk:
            return '-'
        rv = ', '.join(self.answers.values_list('text', flat=True))
        if self.text is not None:
            rv += f", other: {self.text}"
        return rv
