from django import template
from gearStore.models import Category, PageContents

register = template.Library()

@register.inclusion_tag('gearStore/category_menu.html')
def get_category_list():
    return {'categories': Category.objects.all()}

@register.inclusion_tag('gearStore/base.html')
def get_categories():
    return {'categories': Category.objects.all()}

@register.inclusion_tag('gearStore/display_title.html')
def get_title():
    content = PageContents.objects.all()
    if content:
        return {"title": content[0].title}
    else:
        return {"title": "Gear Store"}