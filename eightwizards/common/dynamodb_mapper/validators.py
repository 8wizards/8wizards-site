# pylint: disable=all
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Alec Thomas <alec@swapoff.org>
# Copyright (C) 2012 Ludia Inc.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: Alec Thomas <alec@swapoff.org>
# Maintainers: Jean-Tiare Le Bigot <jtlebigot@socialludia.com>,

import os
import re
from urllib.parse import urlparse

from .schema import Schema
from .errors import Invalid, SchemaError, UNDEFINED


# Markers

class Marker(object):
    """Mark nodes for special treatment."""

    def __init__(self, schema, msg=None):
        self.schema = schema
        self._schema = Schema(schema)
        self.msg = msg

    def __call__(self, v):
        try:
            return self._schema(v)
        except Invalid as e:
            if not self.msg or len(e.path) > 1:
                raise
            raise Invalid(self.msg)

    def __str__(self):
        return str(self.schema)

    def __repr__(self):
        return repr(self.schema)


class Optional(Marker):
    """Mark a node in the schema as optional."""


class Required(Marker):
    """Mark a node in the schema as being required."""

    def __init__(self, schema, default=UNDEFINED, msg=None):
        super(Required, self).__init__(schema, msg)
        self.default = default


def extra_validator(_):
    """Allow keys in the data that are not present in the schema."""
    raise SchemaError('"extra" should never be called')


# Validators


def msg_validator(schema, msg):
    """Report a user-friendly message if a schema fails to validate.
    Messages are only applied to invalid direct descendants of the schema.
    """
    schema = Schema(schema)

    def f(v):
        try:
            return schema(v)
        except Invalid as e:
            if len(e.path) > 1:
                raise e
            else:
                raise Invalid(msg)
    return f


def coerce_validator(target_type, msg=None):
    """Coerce a value to a type. If the input value of the validator is already
    of this type, tha value is retured immediately to prevent stupid crash like
    datetime(datime()). This way, ``Coerce`` can safely be used to make sure the
    type is OK.

    If the type constructor throws a ValueError, the value will be marked as
    Invalid.

    :param target_type: target type for the coercion operation. May be any type
    or callable.
    """
    def f(v):
        try:
            if type(v) is target_type:
                return v
            return target_type(v)
        except ValueError:
            raise Invalid(msg or ('Failed to coerce %s of type \'%s\' to \'%s\'' % (repr(v), type(v).__name__,
                                                                                    target_type.__name__)))
    return f


def istrue_validator(msg=None):
    """Assert that a value is true, in the Python sense.
    "In the Python sense" means that implicitly false values, such as empty
    lists, dictionaries, etc. are treated as "false":
    """
    def f(v):
        if v:
            return v
        raise Invalid(msg or '%s is not True' % (repr(v)))
    return f


def isfalse_validator(msg=None):
    """Assert that a value is false, in the Python sense.
    """
    def f(v):
        if not v:
            return v
        raise Invalid(msg or '%s is not False' % (repr(v)))
    return f


def boolean_validator(msg=None):
    """Convert human-readable boolean values to a bool.

    Accepted values are 1, true, yes, on, enable, and their negatives.
    Non-string values are cast to bool.
    """
    def f(v):
        try:
            if isinstance(v, str):
                v = v.lower()
                if v in ('1', 'true', 'yes', 'on', 'enable'):
                    return True
                if v in ('0', 'false', 'no', 'off', 'disable'):
                    return False
                raise Invalid(msg or ('Failed to parse %s of type \'%s\' as Boolean' % (repr(v), type(v).__name__)))
            return bool(v)
        except ValueError:
            raise Invalid(msg or ('Failed to parse %s of type \'%s\' as Boolean' % (repr(v), type(v).__name__)))
    return f


def any_validator(*validators, **kwargs):
    """Use the first validated value.

    :param msg: Message to deliver to user if validation fails.
    :returns: Return value of the first validator that passes.
    """
    msg = kwargs.pop('msg', None)
    schemas = [Schema(val) for val in validators]

    def f(v):
        for schema in schemas:
            try:
                return schema(v)
            except Invalid as e:
                if len(e.path) > 1:
                    raise
                pass  # pragma: no coverage (still and again a coverage bug)
        else:
            raise Invalid(msg or 'no validator matched for %s of type \'%s\'' % (repr(v), type(v).__name__))
    return f


def all_validator(*validators, **kwargs):
    """Value must pass all validators.

    The output of each validator is passed as input to the next.

    :param msg: Message to deliver to user if validation fails.
    """
    msg = kwargs.pop('msg', None)
    schemas = [Schema(val) for val in validators]

    def f(v):
        try:
            for schema in schemas:
                v = schema(v)
        except Invalid as e:
            raise Invalid(msg or e.msg)
        return v
    return f


def match_validator(pattern, msg=None):
    """Value must match the regular expression.

    Pattern may also be a compiled regular expression:
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern)

    def f(v):
        if not pattern.match(v):
            raise Invalid(msg or '%s does not match regular expression %s' % (repr(v), type(v).__name__))
        return v
    return f


def sub_validator(pattern, substitution):
    """Regex substitution.
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern)

    def f(v):
        return pattern.sub(substitution, v)
    return f


def url_validator(msg=None):
    """Verify that the value is a URL."""
    def f(v):
        try:
            urlparse(v)
            return v
        except:
            raise Invalid(msg or '%s does not look like a valid URL' % (repr(v)))
    return f


def isfile_validator(msg=None):
    """Verify the file exists."""
    def f(v):
        if os.path.isfile(v):
            return v
        else:
            raise Invalid(msg or '%s does not point to a file' % (repr(v)))
    return f


def isdir_validator(msg=None):
    """Verify the directory exists."""
    def f(v):
        if os.path.isdir(v):
            return v
        else:
            raise Invalid(msg or '%s does not point to a directory' % (repr(v)))
    return f


def patchexists_validator(msg=None):
    """Verify the path exists, regardless of its type."""
    def f(v):
        if os.path.exists(v):
            return v
        else:
            raise Invalid(msg or '%s does not exist on filesystem' % (repr(v)))
    return f


def inrange_validator(min=None, max=None, msg=None):
    """Limit a value to a range.

    Either min or max may be omitted.

    :raises Invalid: If the value is outside the range and clamp=False.
    """
    def f(v):
        if min is not None and v < min:
            raise Invalid(msg or 'value must be at least %s. Got %s' % (min, repr(v)))
        if max is not None and v > max:
            raise Invalid(msg or 'value must be at most %s. Got %s' % (max, repr(v)))
        return v
    return f


def clamp_validator(min=None, max=None, msg=None):
    """Clamp a value to a range.

    Either min or max may be omitted.
    """
    def f(v):
        if min is not None and v < min:
            v = min
        if max is not None and v > max:
            v = max
        return v
    return f


def length_validator(min=None, max=None, msg=None):
    """The length of a value must be in a certain range."""
    def f(v):
        if min is not None and len(v) < min:
            raise Invalid(msg or 'length of value must be at least %s. Got %s of length %s' % (min, repr(v), len(v)))
        if max is not None and len(v) > max:
            raise Invalid(msg or 'length of value must be at most %s. Got %s of length %s' % (max, repr(v), len(v)))
        return v
    return f


# weird calling convention...

def to_lower(v):
    """Transform a string to lower case.
    """
    return str(v).lower()


def to_upper(v):
    """Transform a string to upper case.
    """
    return str(v).upper()


def capitalize(v):
    """Capitalise a string.
    """
    return str(v).capitalize()


def title(v):
    """Title case a string.
    """
    return str(v).title()

