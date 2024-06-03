# -*- coding: utf-8 -*-
# SMSC.RU API (smsc.ru) версия 2.0 (03.07.2019)

from datetime import datetime
from time import sleep
import smtplib

try:
    from urllib import urlopen, quote
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import quote

# Константы для настройки библиотеки
SMSC_LOGIN = "your_smsc_login"    # логин клиента
SMSC_PASSWORD = "your_smsc_password"  # пароль
SMSC_POST = True                  # использовать метод POST
SMSC_HTTPS = False                 # использовать HTTPS протокол
SMSC_CHARSET = "utf-8"             # кодировка сообщения (windows-1251 или koi8-r), по умолчанию используется utf-8
SMSC_DEBUG = True                  # флаг отладки

# Константы для отправки SMS по SMTP
SMTP_FROM = "api@smsc.ru"          # e-mail адрес отправителя
SMTP_SERVER = "send.smsc.ru"       # адрес smtp сервера
SMTP_LOGIN = ""                    # логин для smtp сервера
SMTP_PASSWORD = ""                 # пароль для smtp сервера

# Вспомогательная функция, эмуляция тернарной операции ?:
def ifs(cond, val1, val2):
    if cond:
        return val1
    return val2


# Класс для взаимодействия с сервером smsc.ru
class SMSC(object):

    # Метод отправки SMS
    def send_sms(self, phones, message, translit=0, time="", id=0, format=0, sender=False, query=""):
        formats = ["flash=1", "push=1", "hlr=1", "bin=1", "bin=2", "ping=1", "mms=1", "mail=1", "call=1", "viber=1", "soc=1"]

        m = self._smsc_send_cmd("send", "cost=3&phones=" + quote(phones) + "&mes=" + quote(message) + \
                    "&translit=" + str(translit) + "&id=" + str(id) + ifs(format > 0, "&" + formats[format-1], "") + \
                    ifs(sender == False, "", "&sender=" + quote(str(sender))) + \
                    ifs(time, "&time=" + quote(time), "") + ifs(query, "&" + query, ""))

        # (id, cnt, cost, balance) или (id, -error)
        if SMSC_DEBUG:
            if m[1] > "0":
                print("Сообщение отправлено успешно. ID: " + m[0] + ", всего SMS: " + m[1] + ", стоимость: " + m[2] + ", баланс: " + m[3])
            else:
                print("Ошибка №" + m[1][1:] + ifs(m[0] > "0", ", ID: " + m[0], ""))

        return m

    # SMTP версия метода отправки SMS
    def send_sms_mail(self, phones, message, translit=0, time="", id=0, format=0, sender=""):
        server = smtplib.SMTP(SMTP_SERVER)

        if SMSC_DEBUG:
            server.set_debuglevel(1)

        if SMTP_LOGIN:
            server.login(SMTP_LOGIN, SMTP_PASSWORD)

        server.sendmail(SMTP_FROM, "send@send.smsc.ru", "Content-Type: text/plain; charset=" + SMSC_CHARSET + "\n\n" + \
                            SMSC_LOGIN + ":" + SMSC_PASSWORD + ":" + str(id) + ":" + time + ":" + str(translit) + "," + \
                            str(format) + "," + sender + ":" + phones + ":" + message)
        server.quit()

    # Метод получения стоимости SMS
    def get_sms_cost(self, phones, message, translit=0, format=0, sender=False, query=""):
        formats = ["flash=1", "push=1", "hlr=1", "bin=1", "bin=2", "ping=1", "mms=1", "mail=1", "call=1", "viber=1", "soc=1"]

        m = self._smsc_send_cmd("send", "cost=1&phones=" + quote(phones) + "&mes=" + quote(message) + \
                    ifs(sender == False, "", "&sender=" + quote(str(sender))) + \
                    "&translit=" + str(translit) + ifs(format > 0, "&" + formats[format-1], "") + ifs(query, "&" + query, ""))

        # (cost, cnt) или (0, -error)
        if SMSC_DEBUG:
            if m[1] > "0":
                print("Стоимость рассылки: " + m[0] + ". Всего SMS: " + m[1])
            else:
                print("Ошибка №" + m[1][1:])

        return m

    # Метод проверки статуса отправленного SMS или HLR-запроса
    def get_status(self, id, phone, all=0):
        m = self._smsc_send_cmd("status", "phone=" + quote(phone) + "&id=" + str(id) + "&all=" + str(all))

        # (status, time, err, ...) или (0, -error)
        if SMSC_DEBUG:
            if m[1] >= "0":
                tm = ""
                if m[1] > "0":
                    tm = str(datetime.fromtimestamp(int(m[1])))
                print("Статус SMS = " + m[0] + ifs(m[1] > "0", ", время изменения статуса - " + tm, ""))
            else:
                print("Ошибка №" + m[1][1:])

        if all and len(m) > 9 and (len(m) < 14 or m[14] != "HLR"):
            m = (",".join(m)).split(",", 8)

        return m

    # Метод получения баланса
    def get_balance(self):
        m = self._smsc_send_cmd("balance") # (balance) или (0, -error)

        if SMSC_DEBUG:
            if len(m) < 2:
                print("Сумма на счете: " + m[0])
            else:
                print("Ошибка №" + m[1][1:])

        return ifs(len(m) > 1, False, m[0])

    # ВНУТРЕННИЕ МЕТОДЫ
    def _smsc_send_cmd(self, cmd, arg=""):
        url = ifs(SMSC_HTTPS, "https", "http") + "://smsc.ru/sys/" + cmd + ".php"
        _url = url
        arg = "login=" + quote(SMSC_LOGIN) + "&psw=" + quote(SMSC_PASSWORD) + "&fmt=1&charset=" + SMSC_CHARSET + "&" + arg

        i = 0
        ret = ""

        while ret == "" and i <= 5:
            if i > 0:
                url = _url.replace("smsc.ru/", "www" + str(i) + ".smsc.ru/")
            else:
                i += 1

            try:
                if SMSC_POST or len(arg) > 2000:
                    data = urlopen(url, arg.encode(SMSC_CHARSET))
                else:
                    data = urlopen(url + "?" + arg)

                ret = str(data.read().decode(SMSC_CHARSET))
            except:
                ret = ""

            i += 1

        if ret == "":
            if SMSC_DEBUG:
                print("Ошибка чтения адреса: " + url)
            ret = "," # фиктивный ответ

        return ret.split(",")
