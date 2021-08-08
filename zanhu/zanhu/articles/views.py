from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from zanhu.articles.models import Article
from zanhu.articles.forms import ArticleForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from zanhu.helpers import AuthorRequireMixin


class ArticlesListView(LoginRequiredMixin, ListView):
    """
    已发表文章列表
    get_context_data 方法，这个方法是用来给传递到模板文件的上下文对象
    而 context_object_name 是给 get_queryset 方法返回的 model 列表重新命名的
    """
    model = Article
    paginate_by = 10
    context_object_name = "articles"
    template_name = "articles/article_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


class DraftListView(ArticlesListView):
    """
    草稿箱文章列表
    """
    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).get_drafts()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    发表文章
    """
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_create.html"
    message = "您的文章已创建成功！"
    initial = {"title" : "ok"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        创建成功后跳转
        :return:
        """
        messages.success(self.request, self.message)
        return reverse_lazy("articles:list")

    def get_initial(self):
        initial = super().get_initial()
        return initial


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """
    文章详情
    """
    model = Article
    template_name = "articles/article_detail.html"


class ArticleEditView(LoginRequiredMixin, AuthorRequireMixin, UpdateView):
    """
    编辑文章
    """
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_update.html"
    message = "您的文章已修改成功！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("articles:article", kwargs={"slug":self.get_object().slug})







