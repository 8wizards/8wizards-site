import logging
from importlib import import_module
from rest_framework.routers import BaseRouter, DefaultRouter
from django.apps import apps

logger = logging.getLogger(__name__)


class SharedRootDefaultRouter(DefaultRouter):
    """
    Adds a register_router method to DefaultRouter which clones
    registry entries from a sub-router into this router so that
    all share a common root namespace.
    """

    def register_router(self, router):
        """
        Clone a router's registry into this router.
        """
        for prefix, viewset, basename in router.registry:
            self.register(prefix, viewset, base_name=basename)


def _try_import_api(app):
    """
    Attempts to import api.py for the specified app.
    :param app: app name
    :return: api module, or None if not found
    """
    module_name = '{}.api'.format(app)
    try:
        return import_module(module_name)
    except ImportError as err:
        if err.name == module_name:
            # import error trying to load requested module -- skip quietly as this failure is normal
            logger.debug('skipping "%s" which does not contain an api module', app)
        else:
            # import error while trying to import something *inside* the requested module
            # don't eat this error as this is a programming error
            raise err

    return None


def _try_get_router(app, api_module):
    """
    Attempts to get the 'router' from the specified api_module.
    :param api_module: api module to search
    :return: router, or None if not found or invalid
    """
    if not api_module:
        return

    router = getattr(api_module, 'router', None)

    if not router:
        logger.warn('%s contains an api module but it is missing a "router" variable.', app)
        return None

    if not isinstance(router, BaseRouter):
        logger.warn('%s contains an api.router, but the router is not derived from BaseRouter', app)
        return None

    return router


def autodiscover_api_routers():
    """
    Searches for api_routers in apps included in the app registry
    and returns a SharedRootDefaultRouter containing each of the
    discovered routers.

    Looks for a variable named "router" in an "api" module in
    each app.
    """
    # TODO: Support multiple API versions by allowing "router" to contain a dictionary
    api_router = SharedRootDefaultRouter()

    for app_config in apps.get_app_configs():
        app = app_config.name
        if app.startswith('django.'):
            # skip Django core apps to avoid false warnings
            continue

        api_module = _try_import_api(app)
        router = _try_get_router(app, api_module)
        if router:
            # if router is not None it is good
            api_router.register_router(router)
            logger.debug('registered "%s"', app_config.name)

    return api_router

