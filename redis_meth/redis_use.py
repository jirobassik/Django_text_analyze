from django.core.cache import cache

#CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# def cached_sample():
#     if 'sample' in cache:
#         json = cache.get('sample')
#         return JsonResponse(json, safe=False)
#     else:
#         objs = OwnerModel.objects.all()
#         json = serializers.serialize('json', objs)
#         # store data in cache
#         cache.set('sample', json, timeout=CACHE_TTL)
#         return JsonResponse(json, safe=False)

def set_key(key, value, timeout=None):
    return cache.set(key, value, timeout=timeout)

def add_key(key, value, timeout=None):
    return cache.add(key, value, timeout=timeout)

def get_key(key):
    return cache.get(key)

def delete_key(key):
    return cache.delete(key)
