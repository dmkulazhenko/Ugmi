# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse, urljoin
from flask import request, url_for
from config import SMALL_MARKS_DIR, temp_dir


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def init_Ugmi():
    if not os.path.isdir(SMALL_MARKS_DIR):
        os.mkdir(SMALL_MARKS_DIR)
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
