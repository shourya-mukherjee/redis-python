import time

class TTLCache:
    def __init__(self):
        self.h = {}
        self.expiry_times = {}
    
    def set(self, key, val, ttl=None):
        self.h[key] = val
        if ttl:
            self.expiry_times[key] = self._timer() + ttl
        self._clean()
    
    def get(self, key):
        print(self._timer(), self.expiry_times)
        if key in self.h:
            if key in self.expiry_times and self._is_expired(key):
                del self.h[key]
                del self.expiry_times[key]
                return None
            return self.h[key]
        return None

    def _timer(self):
        return time.monotonic() * 1000
    
    def _clean(self):
        expired_keys = [key for key in self.h if self._is_expired(key)]
        for key in expired_keys:
            del self.h[key]
            del self.expiry_times[key]

    def _is_expired(self, key):
        if key in self.expiry_times:
            return self.expiry_times[key] < self._timer()
        return False