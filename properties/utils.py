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
    """
    Retrieve Redis cache hit and miss metrics, calculate hit ratio,
    log them, and return as a dictionary.
    """
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0.0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }

    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics
