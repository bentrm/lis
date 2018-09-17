"""Custom throttling implementation that is will be used for educational purposes."""

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle


class ApiKeyThrottle(BaseThrottle):
    """Custom API throttling implementation that maps API keys to rates."""

    rate = 10
    time_to_live = 10

    def allow_request(self, request, view):
        """Return True if rate has not been exceeded."""
        key = request.META.get("HTTP_API_KEY", "")
        if key:
            rate = cache.get_or_set(key, 0, self.time_to_live)
            print(cache.get(key))
            if rate >= self.rate:
                return False
            else:
                cache.incr(key)
        return True
