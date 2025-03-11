from django import template
from django.utils.safestring import mark_safe
from ..models import StaticPage

register = template.Library()

@register.inclusion_tag('staticpage/chunk/menu_li.html', takes_context=True)
def render_menu_static(context):
    request = context['request']
    menu = StaticPage.objects.filter(is_draft=True)
    return {
        'menu': menu,
        'current_url': request.path,  # Передаем текущий URL в контекст
    }
