from django.core.cache import cache

def set_key(key, value, timeout=None):
    return cache.set(key, value, timeout=timeout)

def set_many_key(timeout=None, **kwargs):
    return cache.set_many(kwargs, timeout)

def add_key(key, value, timeout=None):
    return cache.add(key, value, timeout=timeout)

def get_key(key):
    return cache.get(key)

def delete_key(key):
    return cache.delete(key)
