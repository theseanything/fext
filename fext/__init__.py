# -*- coding: utf-8 -*-

import logging

class NullHandler(logging.Handler):  # pragma: no cover
    def emit(self, record):
        pass

logging.getLogger('fext').addHandler(NullHandler())
