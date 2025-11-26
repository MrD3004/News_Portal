from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Article, Publisher, CustomUser, Newsletter
from .forms import (
    ArticleForm,
    CustomUserCreationForm,
    PublisherForm,
    NewsletterForm,
)
from .serializers import ArticleSerializer


# ---------------------------
# Role check helpers
# ---------------------------
def is_editor(user):
    return user.is_authenticated and getattr(user, "role", None) == "editor"

def is_journalist(user):
    return user.is_authenticated and getattr(user, "role", None) == "journalist"

def is_reader(user):
    return user.is_authenticated and getattr(user, "role", None) == "reader"

def is_publisher(user):
    return user.is_authenticated and getattr(user, "role", None) == "publisher"


# ---------------------------
# User Registration
# ---------------------------
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


# ---------------------------
# Homepage
# ---------------------------
def home(request):
    articles = Article.objects.filter(approved=True).order_by("-id")

    subscribed_publishers = []
    subscribed_journalists = []
    if request.user.is_authenticated and is_reader(request.user):
        subscribed_publishers = request.user.subscribed_publishers.all()
        subscribed_journalists = request.user.subscribed_journalists.all()

    return render(
        request,
        "homepage.html",
        {
            "articles": articles,
            "subscribed_publishers": subscribed_publishers,
            "subscribed_journalists": subscribed_journalists,
        },
    )


# ---------------------------
# Article detail
# ---------------------------
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "article_detail.html", {"article": article})


# ---------------------------
# Create article (journalists only)
# ---------------------------
@login_required
@user_passes_test(is_journalist)
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("journalist_article_list")
    else:
        form = ArticleForm()
    return render(
        request,
        "form.html",
        {
            "form": form,
            "object_name": "Article",
            "cancel_url": "journalist_article_list",
        },
    )


@login_required
@user_passes_test(is_journalist)
def journalist_article_list(request):
    articles = Article.objects.filter(author=request.user).order_by("-created_at")
    return render(
        request,
        "list.html",
        {
            "articles": articles,
            "object_name": "Article",
            "dashboard": False,
        },
    )


# ---------------------------
# Update article (journalists only)
# ---------------------------
@login_required
@user_passes_test(is_journalist)
def journalist_article_update(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("journalist_article_list")
    else:
        form = ArticleForm(instance=article)
    return render(
        request,
        "form.html",
        {
            "form": form,
            "object_name": "Article",
            "cancel_url": "journalist_article_list",
        },
    )


# ---------------------------
# Delete article (journalists only)
# ---------------------------
@login_required
@user_passes_test(is_journalist)
def journalist_article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        article.delete()
        return redirect("journalist_article_list")
    return render(
        request,
        "confirm_delete.html",
        {"article": article, "object_name": "Article", "cancel_url": "journalist_article_list"},
    )


# ---------------------------
# Register publisher (publisher role)
# ---------------------------
@login_required
@user_passes_test(is_publisher)
def register_publisher(request):
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save(commit=False)
            publisher.owner = request.user
            publisher.save()
            return redirect("home")
    else:
        form = PublisherForm()
    return render(request, "register_publisher.html", {"form": form})


# ---------------------------
# Editor dashboard
# ---------------------------
@login_required
@user_passes_test(is_editor)
def editor_dashboard(request):
    # Show only pending (unapproved) articles
    articles = Article.objects.filter(approved=False).order_by("-id")
    return render(
        request,
        "editor_dashboard.html",
        {"articles": articles, "object_name": "Article"},
    )


# ---------------------------
# Journalist dashboard
# ---------------------------
@login_required
@user_passes_test(is_journalist)
def journalist_dashboard(request):
    # Show all articles authored by the logged-in journalist
    articles = Article.objects.filter(author=request.user).order_by("-created_at")
    return render(
        request,
        "journalist_dashboard.html",
        {"articles": articles, "object_name": "Article"},
    )


# ---------------------------
# Publisher dashboard
# ---------------------------
@login_required
@user_passes_test(is_publisher)
def publisher_dashboard(request):
    # Show all articles belonging to publishers owned by this user
    articles = Article.objects.filter(publisher__owner=request.user).order_by("-created_at")
    return render(
        request,
        "publisher_dashboard.html",
        {"articles": articles, "object_name": "Article"},
    )


# ---------------------------
# Approve article (editors only)
# ---------------------------
@login_required
@user_passes_test(is_editor)
def approve_article(request, pk):
    """
    Allows editors to approve an article and optionally post it to Twitter/X.
    """
    article = get_object_or_404(Article, pk=pk)

    if not article.approved:  # prevent re-approving
        article.approved = True
        article.save()

        # Optional Twitter/X integration
        try:
            from .utils import post_to_twitter
            post_to_twitter(article)
        except Exception as e:
            print(f"[Twitter] Post failed: {e}")

    return redirect("editor_dashboard")


# ---------------------------
# Update article (journalists only)
# ---------------------------
@login_required
@user_passes_test(is_journalist)
def journalist_article_update(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()  # author already enforced by query
            return redirect("journalist_article_list")
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "form.html",
        {
            "form": form,
            "object_name": "Article",
            "cancel_url": "journalist_article_list",
            "article": article,
        },
    )


# ---------------------------
# Update article (editors only)
# ---------------------------
@login_required
@user_passes_test(is_editor)
def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)
            # Ensure editor cannot change author
            updated_article.author = article.author
            updated_article.save()
            return redirect("editor_dashboard")
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "form.html",
        {
            "form": form,
            "object_name": "Article",
            "cancel_url": "editor_dashboard",
            "article": article,
        },
    )


# ---------------------------
# Delete article (editors only)
# ---------------------------
@login_required
@user_passes_test(is_editor)
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        # Optional: prevent deletion of already approved articles
        if not article.approved:
            article.delete()
        return redirect("editor_dashboard")
    return render(
        request,
        "confirm_delete.html",
        {"object": article, "object_name": "Article", "cancel_url": "editor_dashboard"},
    )


# ---------------------------
# Newsletter CRUD (journalists only)
# ---------------------------
@login_required
@user_passes_test(is_journalist)
def newsletter_list(request):
    newsletters = (
        Newsletter.objects.filter(author=request.user)
        .prefetch_related("articles")
        .order_by("-created_at")
    )
    return render(
        request,
        "newsletter_list.html",
        {"newsletters": newsletters, "object_name": "Newsletter"},
    )


@login_required
@user_passes_test(is_journalist)
def newsletter_create(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()
            return redirect("newsletter_list")
    else:
        form = NewsletterForm()
    return render(
        request,
        "form.html",
        {"form": form, "object_name": "Newsletter", "cancel_url": "newsletter_list"},
    )

def newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == "POST":
        newsletter.delete()
        return redirect("journalist_newsletter_list")
    # If you want a confirmation page:
    return render(request, "articles/newsletter_confirm_delete.html", {"newsletter": newsletter})



@login_required
@user_passes_test(is_journalist)
def newsletter_update(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user  # ensure author stays correct
            newsletter.save()
            form.save_m2m()  # ✅ now works because articles is in the form
            return redirect("newsletter_list")
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, "articles/newsletter_form.html", {"form": form})


# ---------------------------
# API: Subscribed articles
# ---------------------------
from django.db.models import Q

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_subscribed_articles(request):
    user = request.user
    if is_reader(user):
        articles = Article.objects.filter(
            Q(publisher__in=user.subscribed_publishers.all()) |
            Q(author__in=user.subscribed_journalists.all()),
            approved=True
        ).distinct().order_by("-id")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    return Response({"detail": "Only readers can access subscribed articles."}, status=403)


# ---------------------------
# Subscriptions page
# ---------------------------
@login_required
@user_passes_test(is_reader)
def subscriptions(request):
    publishers = request.user.subscribed_publishers.all()
    journalists = request.user.subscribed_journalists.all()
    return render(
        request,
        "subscriptions.html",
        {"publishers": publishers, "journalists": journalists, "object_name": "Subscription"},
    )


# ---------------------------
# Subscribe / Unsubscribe to publisher
# ---------------------------
@login_required
@user_passes_test(is_reader)
def subscribe_publisher(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    request.user.subscribed_publishers.add(publisher)
    return redirect("subscriptions")

@login_required
@user_passes_test(is_reader)
def unsubscribe_publisher(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    request.user.subscribed_publishers.remove(publisher)
    return redirect("subscriptions")



# ---------------------------
# Subscribe / Unsubscribe to journalist
# ---------------------------
@login_required
@user_passes_test(is_reader)
def subscribe_journalist(request, journalist_id):
    journalist = get_object_or_404(CustomUser, id=journalist_id, role="journalist")
    request.user.subscribed_journalists.add(journalist)
    return redirect("subscriptions")

@login_required
@user_passes_test(is_reader)
def unsubscribe_journalist(request, journalist_id):
    journalist = get_object_or_404(CustomUser, id=journalist_id, role="journalist")
    request.user.subscribed_journalists.remove(journalist)
    return redirect("subscriptions")



       










