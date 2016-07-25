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
# Maintainers: Jean-Tiare Le Bigot <jtlebigot@socialludia.com>, Dmytro Podoprosvietov <dpodoprosvietov@gsngames.com>


class Undefined(object):
    """ Simple class to represent an undefined value (internal usage)
    """
    def __nonzero__(self):
        return False

    def __repr__(self):
        return '...'


UNDEFINED = Undefined()


class Error(Exception):
    """Base validation exception."""


class Invalid(Error):
    """The data was invalid.

    :attr msg: The error message.
    :attr path: The path to the error, as a list of keys in the source data.
    """

    def __init__(self, message, path=None):
        Exception(self, message)
        self.path = path or []

    @property
    def msg(self):
        return self.args[0]

    def __str__(self):
        error_string = Exception.__str__(self)

        if self.path:
            error_string += ' @ data[%s]' % ']['.join(map(repr, self.path))

        return error_string


class InvalidList(Invalid):
    """ List of captures errors for reporting to the end user.

    :attr errors: Array of errors
    :attr msg: Message associated with the first reported error
    :attr path: Path associated with the first reported error
    """
    # FIXME: why keeping a list if we onlt return values about the *first* eror ?
    def __init__(self, errors):
        """ Create a new list of errors.

        :param errors: list of errors to add initially
        """
        if not errors:
            raise ValueError("'errors' array can *not* be empty")
        self.errors = errors[:]

    @property
    def msg(self):
        return self.errors[0].msg

    @property
    def path(self):
        return self.errors[0].path

    def add(self, error):
        """Push an error to the internal list"""
        self.errors.append(error)

    def __str__(self):
        return str(self.errors[0])


class InvalidRegionError(Exception):
    """Raised when ``set_region()`` is called with an invalid region name.
    """


class ResourceNotFoundError(Exception):
    """Raised when some dynamodb resourse is not found - e.g. table does not exist
    """


class SchemaError(Exception):
    """SchemaError exception is raised when a schema consistency check fails.
    Most of the checks are performed in :py:meth:`~.ConnectionBorg.create_table`.

    Common consistency failure includes lacks of ``__table__``, ``__hash_key__``,
    ``__schema__`` definition or when an :py:class:`~.autoincrement_int` ``hash_key``
    is used with a ``range_key``.
    """


class MaxRetriesExceededError(Exception):
    """Raised when a failed operation couldn't be completed after retrying
    ``MAX_RETRIES`` times (e.g. saving an autoincrementing hash_key).
    """


class ConflictError(Exception):
    """Atomic edition failure.
    Raised when an Item has been changed between the read and the write operation
    and this has been forbid by the ``raise_on_conflict`` argument of
    :meth:`DynamoDBModel.save` (i.e. when somebody changed the DB's version of
    your object behind your back).
    """


class OverwriteError(ConflictError):
    """Raised when saving a DynamoDBModel instance would overwrite something
    in the database and we've forbidden that because we believe we're creating
    a new one (see :meth:`DynamoDBModel.save`).
    """


class ValidationError(Exception):
    """Raised when DynomoDB returns Validation Exception for some reason.
    """