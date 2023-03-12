from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import first
from django.template.response import TemplateResponse
from .models import *


def index(request):
    # получаем список элементов меню, у которых нет родителя
    # значит это наши названия меню
    root_menu_items = Item.objects.filter(parent_id__isnull=True)

    main_menu = []
    for menu_item in root_menu_items:
        menu_item_data = Item.objects.get(name=menu_item.name)
        main_menu.append({'id': menu_item_data.id, 'name': menu_item_data.name})

    data = {'main_menu': main_menu}
    return TemplateResponse(request, "index.html", data)


def show(request, id):
    # дерево предков
    item_parents = ItemsTree.objects.filter(child=id).order_by('-depth')
    # и ближайшие потомки
    item_children = Item.objects.filter(parent=id)

    # строим дерево меню
    def get_menu_tree_query(parents, children):
        level = {'name': parents[0].parent, 'id': parents[0].parent.id}
        # идем по родителям
        if len(parents) > 1:
            level['children'] = []
            level['children'].append(get_menu_tree_query(parents[1:], children))
        # добавляем список детей
        else:
            level['children'] = []
            for ch in children:
                level['children'].append({'name': ch.name, 'id': ch.id, 'children': {}})

        return level

    menu = get_menu_tree_query(item_parents, item_children) if len(item_parents) > 0 else []
    name = Item.objects.get(id=id)

    data = {'menu': menu, 'name': name}
    return TemplateResponse(request, "show.html", data)
