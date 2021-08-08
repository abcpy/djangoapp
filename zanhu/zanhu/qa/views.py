from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from zanhu.qa.models import Question, Answer
from zanhu.qa.forms import QuestionForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from zanhu.helpers import AuthorRequireMixin,ajax_required
from django.contrib.auth.decorators import login_required, PermissionDenied
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


class QuestionListView(LoginRequiredMixin, ListView):

    model = Question
    paginate_by = 10
    context_object_name = "questions"
    template_name = "qa/question_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['popular_tags'] = Question.objects.get_counted_tags()
        context['active'] = "all"
        return context


class AnsweredQuestionListView(QuestionListView):
    """
    已有采纳回答的问题
    """
    def get_queryset(self):
        return Question.objects.get_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnsweredQuestionListView, self).get_context_data()
        context['active'] = "answered"
        return context


class UnAnsweredQuestionListView(QuestionListView):
    """
    未有回答的问题
    """

    def get_queryset(self):
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnAnsweredQuestionListView, self).get_context_data()
        context['active'] = "unanswered"
        return context


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = "问题已提交"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("qa:unanswered_q")


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "qa/question_detail.html"
    context_object_name = "question"


class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    template_name = "qa/answer_form.html"
    fields = ["content"]
    message = "答案已提交"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["question_id"]
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("qa:question_detail", kwargs={"pk":self.kwargs["question_id"]})


    """
    用户首次操作： 赞一下或踩一下，创建 .create()
    用户已经点赞，要取消赞： 删除 .delete()
    用户已经赞过，要踩一下： 更新 .update()
    用户已经踩过，要取消踩： 删除 .delete()
    用户已经踩过， 要赞一下： 更新 .update()
  """


@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    question_id = request.POST["question"]
    value = True if request.POST["value"] == "U" else False
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)
    print(users)

    if request.user.pk in users and (question.votes.get(user=request.user)).value == value:
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes":question.total_votes()})

    # # 1. 用户首次操作： 赞一下或踩一下，创建 .create()
    # if request.user.pk not in users:
    #     question.votes.update_or_create(user=request.user, defaults={"value":value})
    #     # question.votes.create(user=request.user, value=value)
    # #用户已经点赞，要取消赞： 删除 .delete()
    # elif question.votes.get(user=request.user).value:
    #     if value:
    #         question.votes.get(user=request.user).delete()
    #     else:
    #         question.votes.update_or_create(user=request.user, defaults={"value": value})
    # # 用户已经踩过，要取消踩： 删除 .delete()
    # #     用户已经踩过， 要赞一下： 更新 .update()
    # else:
    #     if not value:
    #         question.votes.get(user=request.user).delete()
    #     else:
    #         question.votes.update_or_create(user=request.user, defaults={"value": value})

@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_vote(request):
    answer_id = request.POST["answer"]
    value = True if request.POST["value"] == "U" else False
    answer = Answer.objects.get(uuid_id=answer_id)
    users = answer.votes.values_list('user', flat=True)

    if request.user.pk in users and (answer.votes.get(user=request.user)).value == value:
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes":answer.total_votes()})

@login_required
@ajax_required
@require_http_methods(["POST"])
def accept_answer(request):
    """
    接受回答，AJXJ POST请求
    已经被接受的回答用户不能取消
    :param request:
    :return:
    """
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    # 如果当前登录用户不是提问者，抛出权限拒绝错误
    if answer.question.user.username != request.user.username:
        raise PermissionDenied
    answer.accept_answer()
    return JsonResponse({"status":"true"})


























