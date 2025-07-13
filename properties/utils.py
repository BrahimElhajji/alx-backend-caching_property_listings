# properties/utils.py

from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging


logger = logging.getLogger(__name__)


def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values())
        cache.set('all_properties', properties, 3600)  # 1 hour
    return properties


def get_redis_cache_metrics():
    redis_client = get_redis_connection("default")
    info = redis_client.info("stats")
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests > 0 else 0

    logger.error(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio
    }
