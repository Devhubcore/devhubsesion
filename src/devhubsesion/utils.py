import os
import re
from datetime import datetime

_bad = re.compile(r'[<>:"/\\|?*\[\](){} \'\t\n\r]')

phones = [
    r'0[0-9]{10,11}',
    r'\+98[0-9]{10,11}',
    r'0098[0-9]{10,11}',
    r'[0-9]{4,5}[-][0-9]{4,6}',
]


def clean(name):
    return _bad.sub('_', name or "no_name")


def mkdir(path):
    os.makedirs(path, exist_ok=True)
    return path


def now():
    return datetime.now().strftime('%Y%m%d_%H%M%S')
