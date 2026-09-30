"""Finite-retry BaoStock session lifecycle wrapper (does not modify BaoStock)."""
from __future__ import annotations
import time

SESSION_CODE = "10001001"
class BaoStockSessionManager:
    def __init__(self, client, refresh_interval_seconds=600, max_retries=3, sleep=time.sleep, clock=time.time):
        self.client=client; self.refresh_interval_seconds=refresh_interval_seconds; self.max_retries=max_retries; self.sleep=sleep; self.clock=clock; self.last_login_time=None
    def login(self):
        result=self.client.login()
        if str(getattr(result,'error_code',''))!='0': raise RuntimeError(getattr(result,'error_msg','login failed'))
        self.last_login_time=self.clock(); return result
    def logout(self):
        try: self.client.logout()
        except Exception: pass
    def reconnect(self):
        self.logout(); return self.login()
    def ensure_login(self):
        if self.last_login_time is None: return self.login()
        if self.clock()-self.last_login_time >= self.refresh_interval_seconds: return self.reconnect()
        return None
    @staticmethod
    def classify(result):
        code=str(getattr(result,'error_code','')); msg=str(getattr(result,'error_msg',''))
        if code==SESSION_CODE or '用户未登录' in msg: return 'SESSION_EXPIRED'
        if code.startswith('1'): return 'API_ERROR'
        return 'OK' if code=='0' else 'NETWORK_RETRYABLE'
    def request(self, fn, *args, **kwargs):
        self.ensure_login()
        for attempt in range(self.max_retries+1):
            result=fn(*args,**kwargs); kind=self.classify(result)
            if kind=='OK': return result
            if kind!='SESSION_EXPIRED' and kind!='NETWORK_RETRYABLE': return result
            if attempt >= self.max_retries: return result
            self.sleep(2**attempt)
            self.reconnect()
        return result
