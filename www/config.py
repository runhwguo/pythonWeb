#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration
"""

import www.config_default as config_default
import www.config_override as config_override

__author__ = 'RunhwGuo'


class Dict(dict):
    """
    Simple dict but support access as x.y style.
    """

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def to_dict(d):
    result = Dict()
    for k, v in d.items():
        result[k] = to_dict(v) if isinstance(v, dict) else v
    return result


configs = config_default.configs

try:
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = to_dict(configs)
