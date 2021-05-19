from django import template
from famous_physicists.models import *

register = template.Library()


@register.simple_tag(name='get_cats')
def get_categories():
    return Category.objects.all()
