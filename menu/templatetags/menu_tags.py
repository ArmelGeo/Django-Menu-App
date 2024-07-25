from django import template
from django.template.loader import render_to_string
from menu.models import Menu, MenuItem
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    if not request:
        return ''
    
    try:
        menu = Menu.objects.get(name=menu_name)
        menu_items = MenuItem.objects.filter(menu=menu).prefetch_related('children')
        return mark_safe(render_menu(menu_items, request.path))
    except Menu.DoesNotExist:
        return ''

def render_menu(menu_items, current_url):
    def build_tree(items, parent=None):
        tree = []
        for item in items:
            if item.parent == parent:
                children = build_tree(items, item)
                tree.append((item, children))
        return tree

    menu_tree = build_tree(menu_items)
    return render_menu_items(menu_tree, current_url)

def render_menu_items(menu_tree, current_url):
    html = '<ul>'
    for item, children in menu_tree:
        active = 'active' if item.get_url() == current_url else ''
        html += f'<li class="{active}"><a href="{item.get_url()}">{item.title}</a>'
        if children:
            html += render_menu_items(children, current_url)
        html += '</li>'
    html += '</ul>'
    return html
