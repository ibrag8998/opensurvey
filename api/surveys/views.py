from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from commons.utils import is_swagger_fake_view
from surveys.models import Survey, Question, UserAnswer
from surveys.serializers import SurveySerializer, QuestionPolymorphicSerializer, UserAnswerPolymorphicSerializer, \
    SurveyResultsSerializer
from surveys.utils import qa_mapping


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    @action(['get'], detail=True, serializer_class=SurveyResultsSerializer)
    def results(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class QuestionViewSet(ReadOnlyModelViewSet):
    serializer_class = QuestionPolymorphicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if is_swagger_fake_view(self):
            return Question.objects.all()
        return Question.objects.filter(survey=self.kwargs['survey_pk'])


class UserAnswerViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):  # no update
    serializer_class = UserAnswerPolymorphicSerializer

    def create(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, pk=self.kwargs['survey_pk'])

        if not survey.is_started():
            return Response({"detail": "survey has not started"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if survey.is_ended():
            return Response({"detail": "survey is ended"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return super().create(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # validate if survey with survey_pk from url contains question with question_pk from url
        self.question = get_object_or_404(Question, id=kwargs['question_pk'], survey_id=kwargs['survey_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if is_swagger_fake_view(self):
            return UserAnswer.objects.all()
        return qa_mapping.get_answer_model(self.question).objects.filter(question=self.question)

    def perform_create(self, serializer):
        serializer.save(question=self.question)
