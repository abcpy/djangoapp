from django.urls import path

from zanhu.qa.views import QuestionListView, AnsweredQuestionListView, \
    UnAnsweredQuestionListView,CreateQuestionView,QuestionDetailView, CreateAnswerView, question_vote,answer_vote,accept_answer


app_name = "qa"
urlpatterns = [
    path("", view=QuestionListView.as_view(), name="all_q"),
    path("answered/", view=AnsweredQuestionListView.as_view(), name="answered_q"),
    path("indexed/", view=UnAnsweredQuestionListView.as_view(), name="unanswered_q"),
    path("ask-question/", view=CreateQuestionView.as_view(), name="ask_question"),
    path("question-detail/<int:pk>/", view=QuestionDetailView.as_view(), name="question_detail"),
    path("proposes-answer/<int:question_id>", view=CreateAnswerView.as_view(), name="propose_answer"),
    path("question/vote/", view=question_vote, name="question_vote"),
    path("answer/vote/", view=answer_vote, name="answer_vote"),
    path("accept-answer/", view=accept_answer, name="accept_answer")

]

