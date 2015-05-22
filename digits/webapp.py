# Copyright (c) 2014-2015, NVIDIA CORPORATION.  All rights reserved.

import os
import sys

from flask import Flask
from flask.ext.socketio import SocketIO

from digits import utils
from config import config_option
import digits.scheduler

### Create Flask, Scheduler and SocketIO objects

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = config_option('secret_key')
app.url_map.redirect_defaults = False
socketio = SocketIO(app)
scheduler = digits.scheduler.Scheduler(config_option('gpu_list'))

# Set up flask API documentation, if installed
try:
    from flask.ext.autodoc import Autodoc
    _doc = Autodoc(app)
    autodoc = _doc.doc # decorator
except ImportError:
    print 'ImportError'
    def autodoc():
        def _doc(f):
            # noop decorator
            return f
        return _doc

### Register filters and views

app.jinja_env.globals['server_name'] = config_option('server_name')
app.jinja_env.filters['print_time'] = utils.time_filters.print_time
app.jinja_env.filters['print_time_diff'] = utils.time_filters.print_time_diff
app.jinja_env.filters['print_time_since'] = utils.time_filters.print_time_since
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

import digits.views

### Setup the environment

scheduler.load_past_jobs()

