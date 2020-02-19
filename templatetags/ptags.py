from django import template
#from projekt47.models import Addon
register = template.Library()


@register.inclusion_tag('projekt47/card.html')
def addon_thumb(addon):
    """ transforms an addon into an bootstrap card
    """
    ctx = {
        'title': addon.name,
        'subtitle': f'Autor: {addon.owner}',
        'urls': [{'href': addon.id, 'link': 'Mehr..'}],
        'class': 'addon-thumb',
        'text': addon.text,
    }
    return ctx
