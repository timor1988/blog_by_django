from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from DUEditor.models import UEditorField
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext, gettext_lazy as _
import uuslug


class MyTag(TagBase):
    # 这一步是关键 要设置allow_unicode=True 这样这个字段才能支持中文
    slug = models.SlugField(verbose_name=_("slug"), unique=True, max_length=100, allow_unicode=True)

    # 这个方法也是要覆盖的，它是用来计算slug的，也是添加allow_unicode=True参数
    def slugify(self, tag, i=None):
        slug = slugify(tag, allow_unicode=True)
        if i is not None:
            slug += "_%d" % i
        return slug

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        app_label = "taggit"


class TaggedWhatever(GenericTaggedItemBase):
    # 把我们自定义的模型传递进来，它就能知道如何处理
    tag = models.ForeignKey(
        MyTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250, verbose_name='文章标题')
    slug = models.SlugField(verbose_name="别名", max_length=250, null=True, blank=True)
    category = models.ForeignKey('PostCategory', on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(through=TaggedWhatever)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='作者')
    thumbnail = models.URLField(verbose_name="封面链接", null=True, blank=True)
    desc = models.CharField(max_length=200, verbose_name="摘要", null=True, blank=True)
    body = UEditorField(verbose_name='文章内容', width=960, height=600)
    publish = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='文章状态')

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuslug.slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类")

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Banner(models.Model):
    name = models.CharField(max_length=200, verbose_name="幻灯片名称")
    priority = models.IntegerField(default=0, verbose_name="优先级")
    image_url = models.URLField(verbose_name="图片地址")
    link_to = models.URLField(verbose_name="跳转链接")
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '幻灯片'
        verbose_name_plural = verbose_name
        ordering = ['-priority']