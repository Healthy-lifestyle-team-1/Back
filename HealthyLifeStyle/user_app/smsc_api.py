# Python class to send SMS via smsc.ru API
import urllib.parse
import urllib.request
import json


class SMSC:
    def __init__(self, login=None, password=None):
        from django.conf import settings
        self.login = login or settings.SMSC_LOGIN
        self.password = password or settings.SMSC_PASSWORD
        self.post = settings.SMSC_POST
        self.https = settings.SMSC_HTTPS
        self.charset = settings.SMSC_CHARSET
        self.debug = settings.SMSC_DEBUG

    def send_sms(self, phones, message, sender=None, query=''):
        values = {
            'login': self.login,
            'psw': self.password,
            'phones': phones,
            'mes': message,
            'sender': sender,
            'fmt': 3,
            'charset': self.charset,
            'cost': 3,
            'test': self.debug,
            'op': query
        }
        
        url = f"{'https' if self.https else 'http'}://smsc.ru/sys/send.php"
        data = urllib.parse.urlencode(values).encode('utf-8')

        request = urllib.request.Request(url, data)
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode('utf-8'))

        if self.debug:
            print(f"SMSC send response: {result}")
            print(message)
        
        return result

    def get_balance(self):
        values = {
            'login': self.login,
            'psw': self.password,
            'fmt': 3,
            'charset': self.charset,
        }
        
        url = f"{'https' if self.https else 'http'}://smsc.ru/sys/balance.php"
        data = urllib.parse.urlencode(values).encode('utf-8')

        request = urllib.request.Request(url, data)
        response = urllib.request.urlopen(request)
        result = json.loads(response.read().decode('utf-8'))

        if self.debug:
            print(f"SMSC balance response: {result}")
        
        return result
