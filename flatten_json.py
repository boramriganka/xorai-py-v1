#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:56:27 2020

@author: jharnadohotia
"""
#libraries for JSON parsing function
from functools import (partial,
                       singledispatch)
from itertools import chain
from typing import (Dict,
                    List,
                    TypeVar)

Serializable = TypeVar('Serializable', None, int, bool, float, str, 
                       dict, list, tuple)
Array = List[Serializable]
Object = Dict[str, Serializable]


def flatten(object_: Object,
            *,
            path_separator: str = '.') -> Array[Object]:
    """
    Flattens given JSON object into list of objects with non-nested values.

    >>> flatten({'a': 1})
    [{'a': 1}]
    >>> flatten({'a': [1, 2]})
    [{'a': 1}, {'a': 2}]
    >>> flatten({'a': {'b': None}})
    [{'a.b': None}]
    """
    keys = set(object_)
    result = [dict(object_)]
    while keys:
        key = keys.pop()
        new_result = []
        for index, record in enumerate(result):
            try:
                value = record[key]
            except KeyError:
                new_result.append(record)
            else:
                if isinstance(value, dict):
                    del record[key]
                    new_value = flatten_nested_objects(
                            value,
                            prefix=key + path_separator,
                            path_separator=path_separator)
                    keys.update(new_value.keys())
                    new_result.append({**new_value, **record})
                elif isinstance(value, list):
                    del record[key]
                    new_records = [
                        flatten_nested_objects(sub_value,
                                               prefix=key + path_separator,
                                               path_separator=path_separator)
                        for sub_value in value]
                    keys.update(chain.from_iterable(map(dict.keys,
                                                        new_records)))
                    new_result.extend({**new_record, **record}
                                      for new_record in new_records)
                else:
                    new_result.append(record)
        result = new_result
    return result


@singledispatch
def flatten_nested_objects(object_: Serializable,
                           *,
                           prefix: str = '',
                           path_separator: str) -> Object:
    return {prefix[:-len(path_separator)]: object_}


@flatten_nested_objects.register(dict)
def _(object_: Object,
      *,
      prefix: str = '',
      path_separator: str) -> Object:
    result = dict(object_)
    for key in list(result):
        result.update(flatten_nested_objects(result.pop(key),
                                             prefix=(prefix + key
                                                     + path_separator),
                                             path_separator=path_separator))
    return result


@flatten_nested_objects.register(list)
def _(object_: Array,
      *,
      prefix: str = '',
      path_separator: str) -> Object:
    return {prefix[:-len(path_separator)]: list(map(partial(
            flatten_nested_objects,
            path_separator=path_separator),
            object_))}