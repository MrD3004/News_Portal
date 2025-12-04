from django.urls import path

from . import views

urlpatterns = [
    # ---------------------------
    # Homepage & registration
    # ---------------------------
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    # ---------------------------
    # Articles (general)
    # ---------------------------
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
    # ---------------------------
    # Journalist routes
    # ---------------------------
    path(
        "journalist/dashboard/", views.journalist_dashboard, name="journalist_dashboard"
    ),
    path(
        "journalist/articles/",
        views.journalist_article_list,
        name="journalist_article_list",
    ),
    path(
        "journalist/articles/create/",
        views.create_article,
        name="journalist_article_create",
    ),
    path(
        "journalist/articles/<int:pk>/edit/",
        views.journalist_article_update,
        name="journalist_article_update",
    ),
    path(
        "journalist/articles/<int:pk>/delete/",
        views.journalist_article_delete,
        name="journalist_article_delete",
    ),
    path("journalist/articles/create/", views.create_article, name="create_article"),
    # Newsletter CRUD (journalists only)
    path("journalist/newsletters/", views.newsletter_list, name="newsletter_list"),
    path(
        "journalist/newsletters/create/",
        views.newsletter_create,
        name="newsletter_create",
    ),
    path(
        "journalist/newsletters/<int:pk>/edit/",
        views.newsletter_update,
        name="newsletter_update",
    ),
    path(
        "journalist/newsletters/<int:pk>/delete/",
        views.newsletter_delete,
        name="newsletter_delete",
    ),
    # ---------------------------
    # Editor routes
    # ---------------------------
    path("editor/dashboard/", views.editor_dashboard, name="editor_dashboard"),
    path(
        "editor/articles/<int:pk>/approve/",
        views.approve_article,
        name="approve_article",
    ),
    path("editor/articles/<int:pk>/edit/", views.update_article, name="update_article"),
    path(
        "editor/articles/<int:pk>/delete/", views.delete_article, name="delete_article"
    ),
    # ---------------------------
    # Publisher routes
    # ---------------------------
    path("publisher/dashboard/", views.publisher_dashboard, name="publisher_dashboard"),
    path("publisher/register/", views.register_publisher, name="register_publisher"),
    path(
        "publisher/<int:pk>/subscribe/",
        views.subscribe_publisher,
        name="subscribe_publisher",
    ),
    path(
        "publisher/<int:pk>/unsubscribe/",
        views.unsubscribe_publisher,
        name="unsubscribe_publisher",
    ),
    # ---------------------------
    # Journalist subscriptions
    # ---------------------------
    path(
        "journalist/<int:journalist_id>/subscribe/",
        views.subscribe_journalist,
        name="subscribe_journalist",
    ),
    path(
        "journalist/<int:journalist_id>/unsubscribe/",
        views.unsubscribe_journalist,
        name="unsubscribe_journalist",
    ),
    # ---------------------------
    # Subscriptions page
    # ---------------------------
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    # ---------------------------
    # API
    # ---------------------------
    path(
        "api/subscribed-articles/",
        views.get_subscribed_articles,
        name="get_subscribed_articles",
    ),
]
