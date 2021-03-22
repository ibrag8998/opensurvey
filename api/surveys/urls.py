from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from surveys.views import SurveyViewSet, QuestionViewSet, UserAnswerViewSet

survey_router = routers.SimpleRouter()
survey_router.register('surveys', SurveyViewSet)

questions_router = NestedSimpleRouter(survey_router, 'surveys', lookup='survey')
questions_router.register('questions', QuestionViewSet, basename='question')

user_answers_router = NestedSimpleRouter(questions_router, 'questions', lookup='question')
user_answers_router.register('user_answers', UserAnswerViewSet, basename='useranswer')

app_name = 'surveys'

urlpatterns = [
    *survey_router.urls,
    *questions_router.urls,
    *user_answers_router.urls,
]
