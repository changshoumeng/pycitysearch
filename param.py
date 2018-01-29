#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

service_name="pycitysearch"
mode = 0 if sys.platform == "win32" else 1

# log_file = os.path.join(r".", "conf/logging_debug.conf")
log_file = os.path.join(r".", "conf/logging.conf")
# model_dir="/data/cppgroup/work/textwithtags"
citygeo_fn='data/citygeo.txt'
neighbours_fn="data/neighbours.txt"