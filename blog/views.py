from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Post, MyTag, Banner
from .forms import SearchForm
from django.db.models import Q



def blog_index(request):
    objects = Post.published.all()
    posts = objects[:5]
    banners = Banner.objects.all()
    return render(request, 'blog/index.html', {'posts': posts, 'banners': banners})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        # 从MyTag对应的数据库表里查询tag
        tag = get_object_or_404(MyTag, slug=tag_slug)
        # 因为文章和标签是多对多的关系，所以这里要把tag放到列表里面
        # 这里的意思是查询那些文章标签里包含给定标签的文章
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 5)  # 每页5篇文章
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug,
                             status='published')
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/detail.html', {'post': post,
                                                # 'similar_posts': similar_posts,
                                                })


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    context = {}
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.filter(Q(title__contains=query)|Q(body__contains=query))
            paginator = Paginator(results, 5)  # 每页5篇文章
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context['posts'] = posts
            context['page'] = page
            context['query'] = query
    return render(request, 'blog/search.html', context=context)

