import tweepy
from django.conf import settings
from django.contrib.sites.models import Site


def post_to_twitter(article):
    """
    Post a new article announcement to Twitter using Tweepy v2 Client.

    Expects the following settings to be defined in settings.py:
    - TWITTER_API_KEY
    - TWITTER_API_SECRET
    - TWITTER_ACCESS_TOKEN
    - TWITTER_ACCESS_SECRET
    - (optional) TWITTER_BEARER_TOKEN
    - (optional) TWITTER_PREFIX
    - (optional) TWITTER_ENABLED
    """
    if not getattr(settings, "TWITTER_ENABLED", False):
        print("⚠️ Twitter posting is disabled (TWITTER_ENABLED=False).")
        return False

    try:
        # Ensure all required settings exist
        required_keys = [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN",
            "TWITTER_ACCESS_SECRET",
        ]
        for key in required_keys:
            if not getattr(settings, key, None):
                raise ValueError(f"Missing Twitter setting: {key}")

        # Initialize Tweepy v2 Client
        client = tweepy.Client(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_SECRET,
            bearer_token=getattr(settings, "TWITTER_BEARER_TOKEN", None),
        )

        # Build absolute URL
        url = ""
        if hasattr(article, "get_absolute_url"):
            relative_url = article.get_absolute_url()
            site = Site.objects.get_current()
            url = f"https://{site.domain}{relative_url}"

        # Build tweet text
        prefix = getattr(settings, "TWITTER_PREFIX", "📰 New article:")
        tweet_text = f"{prefix} {article.title} {url}".strip()

        # Truncate if needed
        if len(tweet_text) > 280:
            allowed_len = max(0, 276 - len(url))
            tweet_text = f"{prefix} {article.title[:allowed_len]}… {url}"

        # Post tweet
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data.get("id")
        print(f" Tweet posted successfully! Tweet ID: {tweet_id}")
        return tweet_id

    except Exception as e:
        print(f" Twitter post failed: {e}")
        return False



