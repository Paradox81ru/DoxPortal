from django.templatetags.static import static
from django.conf import settings
from django.urls import reverse
from django.utils import translation, timezone
from jinja2 import Environment

from common.template_ext import j_globals
from common.helpers.small.dox_utils import reverse_params


def environment(**options):
    env = Environment(**options)
    # env.install_gettext_callables(gettext=gettext, ngettext=ngettext, newstyle=True)
    env.install_gettext_translations(translation)
    env.globals.update({
        'static': static,
        'url': reverse,
        'url_params': reverse_params,
        'is_debug': lambda: settings.DEBUG,
        'rnd_paradox': j_globals.HeaderParadox.rnd_paradox,
        'today_date': timezone.now(),
        'format_date': j_globals.format_date,
    })
    env.filters.update({
        'format_date': j_globals.format_date,
    })
    return env
