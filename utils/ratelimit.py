from django.core.cache import cache
from django.http import HttpResponseForbidden
from datetime import timedelta
from django.utils import timezone

def ratelimit(max_requests=1, period=timedelta(minutes=1)):  # Changed to 1 per minute
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                identifier = f"user_{request.user.id}" if request.user.is_authenticated else f"ip_{request.META.get('REMOTE_ADDR')}"
                cache_key = f"post_limit_{identifier}"
                
                data = cache.get(cache_key, {'count': 0, 'first_request': timezone.now()})
                
                if timezone.now() > data['first_request'] + period:
                    data = {'count': 0, 'first_request': timezone.now()}
                
                if data['count'] >= max_requests:
                    return HttpResponseForbidden("You can only submit 1 post per minute. Please wait before trying again.")
                
                data['count'] += 1
                cache.set(cache_key, data, timeout=period.total_seconds())
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator