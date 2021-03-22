from django.conf import settings
from django.contrib import admin
from nested_admin.nested import NestedGenericStackedInline, NestedStackedInline
from nested_admin.polymorphic import NestedStackedPolymorphicInline, NestedPolymorphicModelAdmin

from surveys.forms import InputQuestionForm, ChoiceQuestionForm, MultiChoiceQuestionForm, \
    InputChoiceQuestionForm, InputMultiChoiceQuestionForm
from surveys.models import InputQuestion, Answer, ChoiceQuestion, MultiChoiceQuestion, InputChoiceQuestion, \
    InputMultiChoiceQuestion, Question, Survey, UserInputAnswer, UserChoiceAnswer, UserMultiChoiceAnswer, \
    UserInputChoiceAnswer, UserInputMultiChoiceAnswer

if settings.SURVEY_ADMIN_SHOW_USER_ANSWERS:
    class UserInputAnswerInline(NestedStackedInline):
        model = UserInputAnswer
        extra = 0


    class UserChoiceAnswerInline(NestedStackedInline):
        model = UserChoiceAnswer
        extra = 0


    class UserMultiChoiceAnswerInline(NestedStackedInline):
        model = UserMultiChoiceAnswer
        extra = 0


    class UserInputChoiceAnswerInline(NestedStackedInline):
        model = UserInputChoiceAnswer
        extra = 0


    class UserInputMultiChoiceAnswerInline(NestedStackedInline):
        model = UserInputMultiChoiceAnswer
        extra = 0


class AnswerInline(NestedGenericStackedInline):
    model = Answer
    extra = 0
    is_sortable = False
    fk_name = 'question'


class InputQuestionInline(NestedStackedPolymorphicInline.Child):
    model = InputQuestion
    form = InputQuestionForm

    if settings.SURVEY_ADMIN_SHOW_USER_ANSWERS:
        inlines = [UserInputAnswerInline]


class ChoiceQuestionInline(NestedStackedPolymorphicInline.Child):
    model = ChoiceQuestion
    inlines = [AnswerInline]
    form = ChoiceQuestionForm

    if settings.SURVEY_ADMIN_SHOW_USER_ANSWERS:
        inlines += [UserChoiceAnswerInline]


class MultiChoiceQuestionInline(NestedStackedPolymorphicInline.Child):
    model = MultiChoiceQuestion
    inlines = [AnswerInline]
    form = MultiChoiceQuestionForm

    if settings.SURVEY_ADMIN_SHOW_USER_ANSWERS:
        inlines += [UserMultiChoiceAnswerInline]


class InputChoiceQuestionInline(NestedStackedPolymorphicInline.Child):
    model = InputChoiceQuestion
    inlines = [AnswerInline]
    form = InputChoiceQuestionForm

    if settings.SURVEY_ADMIN_SHOW_USER_ANSWERS:
        inlines += [UserInputChoiceAnswerInline]


class InputMultiChoiceQuestionInline(NestedStackedPolymorphicInline.Child):
    model = InputMultiChoiceQuestion
    inlines = [AnswerInline]
    form = InputMultiChoiceQuestionForm

    if settings.SURVEY_ADMIN_SHOW_USER_ANSWERS:
        inlines += [UserInputMultiChoiceAnswerInline]


class QuestionInline(NestedStackedPolymorphicInline):
    sortable_field_name = 'position'
    model = Question
    child_inlines = [
        InputQuestionInline,
        ChoiceQuestionInline,
        MultiChoiceQuestionInline,
        InputChoiceQuestionInline,
        InputMultiChoiceQuestionInline,
    ]

    class Media:
        js = [
            'admin/js/jquery.init.js',
            'polymorphic/js/polymorphic_inlines.js',
            'nested_admin/dist/nested_admin.min.js',
            'surveys/js/ckeditorInitPolymorphicInline.js',
            'surveys/js/collapsedStackedInline.js',
        ]


@admin.register(Survey)
class SurveyAdmin(NestedPolymorphicModelAdmin):
    list_display = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
        ("Даты", {'fields': ['start_at', 'end_at', 'created_at']})
    ]
    inlines = [QuestionInline]
    readonly_fields = ['created_at']
