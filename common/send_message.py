# encoding:utf-8
import requests
from common.dirs import  LOG_FILE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from common.get_secrets import get_secrets
from common.config import conf

import re

def log_reader():
    with open(LOG_FILE, 'r', encoding="UTF-8") as lg:
        logs = lg.readlines()
        logs_str = ''.join(logs).replace("\n","\n\n")
    return logs_str


def send_message(success, message):
    mode = int(conf.get_conf("SendMode")['banksend'])
    if mode == 1:
        title = success and 'GitHub Action Success' or 'GitHub Action Failure'
        # barkurl = get_secrets('BARKURL')
        server_key = get_secrets("SERVERPUSHKEY")
        url = f'https://sctapi.ftqq.com/{server_key}.send?title={title}&desp={message}'
        requests.post(url)

if __name__ == '__main__':
    send_message()
