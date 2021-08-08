from django.db import models
from django.conf import settings
from slugify import slugify
from taggit.managers import TaggableManager
import uuid
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from collections import Counter


class Vote(models.Model):
    """
    使用Django的ContentType, 同时关联用户对问题和回答的投票
    """
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="qa_vote",
                             on_delete=models.CASCADE, verbose_name="用户")
    value = models.BooleanField(default=True, verbose_name="赞同或反对")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="votes_on")
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "投票"
        verbose_name_plural = verbose_name
        unique_together = ["user", "content_type", "object_id"] # 联合唯一键
        # SQL优化
        index_together = ["content_type", "object_id"] # 联合唯一索引


class QuestionQuerySet(models.query.QuerySet):
    """
    自定义QuerySet, 提高模型类的可用性
    """

    def get_answered(self):
        """已有答案的问题"""
        return self.filter(has_answer=True)

    def get_unanswered(self):
        """未被回答的问题"""
        return self.filter(has_answer=False)

    def get_counted_tags(self):
        """统计所有问题标签的数量"""
        tag_dict = {}
        query = self.all().annotate(tagged=models.Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Question(models.Model):
    STATUS = (("O","Open"), ("C", "Close"), ("D", "Draft"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="q_author",
                             on_delete=models.CASCADE, verbose_name="提问者")
    title = models.CharField(max_length=255, unique=True, verbose_name="标题")
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name="(URL)别名")
    status = models.CharField(max_length=1, choices=STATUS,
                              default="O", verbose_name="问题状态")
    content = MarkdownxField(verbose_name="内容")
    tags = TaggableManager(help_text="多个标签使用，（英文）隔开", verbose_name="标签")
    has_answer = models.BooleanField(default=False, verbose_name="接受回答")
    votes = GenericRelation(Vote, verbose_name="投票情况")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        return super(Question, self).save()

    def __str__(self):
        return self.title

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """
        得票数
        :return:
        """
        dic = Counter(self.votes.values_list("value", flat=True))
        return dic[True] - dic[False]

    def get_answer(self):
        """
        获取所有的回答
        :return:
        """
        return Answer.objects.filter(question=self)

    def count_answers(self):
        """
        回答的数量
        :return:
        """
        return self.get_answer().count()

    def get_upvoters(self):
        """
        赞同的用户
        :return:
        """
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        """
        反对的用户
        :return:
        """
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_accepted_answer(self):
        """
        被接受的回答
        :return:
        """
        return Answer.objects.get(question=self, is_answer=True)


class Answer(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='a_author', on_delete=models.CASCADE,
                             verbose_name='回答者')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题")
    content = MarkdownxField(verbose_name="内容")
    is_answer = models.BooleanField(default=False, verbose_name="回答是否被接受")
    votes = GenericRelation(Vote, verbose_name="投票情况")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "回答"
        verbose_name_plural = verbose_name
        ordering = ["-is_answer", "-created_at"] #多字段排序

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """
        得票数
        :return:
        """
        dic = Counter(self.votes.values_list("value", flat=True))
        return dic[True] - dic[False]

    def get_downvoters(self):
        """
        反对的用户
        :return:
        """
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_accepted_answer(self):
        """
        被接受的回答
        :return:
        """
        return Answer.objects.get(question=self.question, is_answer=True)

    def accept_answer(self):
        """
        接受回答 当一个问题有多个回答的时候，只能采纳一个回答，其他的回答一律置为未接受
        :return:
        """
        # 查询当前问题的所有回答
        answer_set = Answer.objects.filter(question=self.question)
        answer_set.update(is_answer=False)
        self.is_answer = True
        self.save()

        #该问题已经有接受被回答的
        self.question.has_answer = True
        self.question.save()





















