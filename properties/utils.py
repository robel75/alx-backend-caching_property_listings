from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if not properties:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, 3600)
    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics.
    """

    redis_client = cache.client.get_client()
    info = redis_client.info()
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0
    
    metrics = {
        'keyspace_hits': hits,
        'keyspace_misses': misses,
        'hit_ratio': hit_ratio,
    }
    logger.info(f"Redis Cache Metrics: {metrics}")
    
    return metrics
