from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, Article, Newsletter


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the CustomUser model with role display.
    """
    model = CustomUser
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Role & Subscriptions", {
            "fields": ("role", "subscribed_publishers", "subscribed_journalists"),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role & Subscriptions", {
            "fields": ("role",),
        }),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Admin for Publisher model.
    """
    list_display = ("name", "owner")
    search_fields = ("name",)
    filter_horizontal = ("editors", "journalists")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin for Article model.
    """
    list_display = ("title", "author", "publisher", "approved", "created_at")
    list_filter = ("approved", "publisher", "created_at")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin for Newsletter model.
    """
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

