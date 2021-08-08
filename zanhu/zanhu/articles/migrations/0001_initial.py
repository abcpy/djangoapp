# Generated by Django 3.2.5 on 2021-07-30 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='标题')),
                ('image', models.ImageField(upload_to='articles_pictures/%Y/%m/%d/', verbose_name='文章图片')),
                ('slug', models.SlugField(max_length=255, verbose_name='(URL)别名')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1, verbose_name='状态')),
                ('content', models.TextField(verbose_name='内容')),
                ('edited', models.BooleanField(default=False, verbose_name='是否可编辑')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('tags', taggit.managers.TaggableManager(help_text='多个标签使用，（英文）隔开', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='标签')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['created_at'],
            },
        ),
    ]
