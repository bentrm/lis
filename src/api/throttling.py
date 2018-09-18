"""Custom throttling implementation that is will be used for educational purposes."""

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle


class ApiKeyThrottle(BaseThrottle):
    """Custom API throttling implementation that maps API keys to rates."""

    caches = ((60, 100), (3600, 10000), (86400, 0))

    @classmethod
    def get_requests_for_api_key(cls, api_key):
        """Return an aggregate list of requests for given api_key."""
        requests = []
        for ttl, max_requests in cls.caches:
            cache_key = f"{api_key}_{ttl}"
            num_requests = cache.get_or_set(cache_key, 0, ttl)
            requests.append((ttl, max_requests, num_requests))
        return requests

    def allow_request(self, request, view):
        """Return True if rate has not been exceeded."""
        api_key = request.META.get("HTTP_API_KEY", "")
        if api_key:
            for ttl, max_requests in self.caches:
                cache_key = f"{api_key}_{ttl}"
                num_requests = cache.get_or_set(cache_key, 0, ttl)
                if max_requests and num_requests >= max_requests:
                    return False
                else:
                    cache.incr(cache_key)
        return True
