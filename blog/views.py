from django.db.models import Count, Prefetch
from django.shortcuts import render, get_object_or_404

from blog.models import Comment, Post, Tag
from sensive_blog.settings import POPULAR_POSTS_PER_PAGE, FRESH_POSTS_PER_PAGE, TAGS_PER_PAGE, POSTS_BY_TAG_PER_PAGE


TAG_PERFETCH = Prefetch(
    'tags',
    queryset=Tag.objects.annotate(related_posts_count=Count('posts'))
)


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.related_posts_count,
    }


def index(request):
    most_popular_posts = Post.objects \
                             .prefetch_related('author', TAG_PERFETCH) \
                             .popular()[:POPULAR_POSTS_PER_PAGE] \
                             .fetch_with_comments_count()

    most_fresh_posts = Post.objects.annotate(comments_count=Count('comments')) \
                           .prefetch_related('author', TAG_PERFETCH) \
                           .order_by('-published_at')[:FRESH_POSTS_PER_PAGE]

    most_popular_tags = Tag.objects.popular()[:TAGS_PER_PAGE]

    context = {
        'most_popular_posts': [serialize_post(post) for post in most_popular_posts],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    # .annotate(comments_count=Count('comments', distinct=True))

    post = get_object_or_404(
        Post.objects.annotate(likes_count=Count('likes')) \
            .prefetch_related('author', TAG_PERFETCH).all(),
        slug=slug
    )

    comments = post.comments.prefetch_related('author').all()
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    related_tags = post.tags.all()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_posts = Post.objects \
                             .prefetch_related('author', TAG_PERFETCH) \
                             .popular()[:POPULAR_POSTS_PER_PAGE] \
                             .fetch_with_comments_count()

    most_popular_tags = Tag.objects.popular()[:TAGS_PER_PAGE]

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [serialize_post(post) for post in most_popular_posts],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = get_object_or_404(
        Tag.objects.annotate(related_posts_count=Count('posts')).all(),
        title=tag_title
    )

    most_popular_posts = Post.objects \
                             .prefetch_related('author', TAG_PERFETCH) \
                             .popular()[:POPULAR_POSTS_PER_PAGE] \
                             .fetch_with_comments_count()

    most_popular_tags = Tag.objects.popular()[:TAGS_PER_PAGE]

    related_posts = tag.posts.annotate(comments_count=Count('comments')) \
                        .prefetch_related('author', TAG_PERFETCH)[:POSTS_BY_TAG_PER_PAGE]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
