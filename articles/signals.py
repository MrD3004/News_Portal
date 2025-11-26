from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Article, Newsletter


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Creates default user groups (Reader, Editor, Journalist) and assigns role-specific permissions
    after migrations for the 'articles' app only.
    """
    if sender.label != "articles":
        return  # Only run for this app

    # Create groups
    reader_group, _ = Group.objects.get_or_create(name="Reader")
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    journalist_group, _ = Group.objects.get_or_create(name="Journalist")

    # Get content types
    article_ct = ContentType.objects.get_for_model(Article)
    newsletter_ct = ContentType.objects.get_for_model(Newsletter)

    # Helper to safely fetch permissions
    def perm(codename, ct):
        return Permission.objects.filter(codename=codename, content_type=ct).first()

    # Assign permissions to Reader
    reader_group.permissions.set([
        p for p in [
            perm("view_article", article_ct),
            perm("view_newsletter", newsletter_ct),
        ] if p
    ])

    # Assign permissions to Editor
    editor_group.permissions.set([
        p for p in [
            perm("change_article", article_ct),
            perm("delete_article", article_ct),
            perm("view_article", article_ct),
            perm("change_newsletter", newsletter_ct),
            perm("delete_newsletter", newsletter_ct),
            perm("view_newsletter", newsletter_ct),
        ] if p
    ])

    # Assign permissions to Journalist
    journalist_group.permissions.set([
        p for p in [
            perm("add_article", article_ct),
            perm("change_article", article_ct),
            perm("delete_article", article_ct),
            perm("view_article", article_ct),
            perm("add_newsletter", newsletter_ct),
            perm("change_newsletter", newsletter_ct),
            perm("delete_newsletter", newsletter_ct),
            perm("view_newsletter", newsletter_ct),
        ] if p
    ])


@receiver(post_save, sender=Article)
def notify_followers_on_approval(sender, instance, created, **kwargs):
    """
    Sends email notifications to readers who follow the journalist
    when an article is approved.
    """
    if instance.approved:
        followers = instance.author.followers.all()
        for user in followers:
            if user.email:
                try:
                    send_mail(
                        subject=f"New Article: {instance.title}",
                        message=instance.content[:200],
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "news@portal.com"),
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"[Email Error] Failed to notify {user.email}: {e}")



