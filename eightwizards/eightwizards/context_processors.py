from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404
from configuration.models import ConfigParam


def site_info(request):
    return {'SITE_INFO': {
            'site_name': ConfigParam.get_param('SEO_SITE_NAME', settings.SITE_VARIABLES.get('site_name')),
            'site_description': ConfigParam.get_param('SEO_SITE_DESCRIPTION', settings.SITE_VARIABLES.get('site_description')),
            'site_keywords': ConfigParam.get_param('SEO_SITE_KEYWORDS', settings.SITE_VARIABLES.get('site_keywords'))
        }}


def url_name(request):
    try:
        match = resolve(request.path)
    except Resolver404:
        return {}
    else:
        namespace, url_name = match.namespace, match.url_name
        if namespace:
            url_name = '%s:%s' % (namespace, url_name)
        return {'URL_NAMESPACE': namespace, 'URL_NAME': url_name}

