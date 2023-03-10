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
    # и ближайшие потомки
    items_list = Item.objects.raw(
        'SELECT items.id id, itemparent.name as show_name, tree.parent_id parent_id, tree.depth depth, 1 as is_parent\
        FROM djangotest_item items\
        JOIN djangotest_itemstree tree\
        ON items.id=tree.child_id \
        JOIN djangotest_item itemparent\
        ON itemparent.id = tree.parent_id\
        WHERE items.id=%s\
        UNION\
        SELECT items.id id, items.name as show_name, items.parent_id parent_id, 1 depth, 0 as is_parent\
        FROM djangotest_item items\
        WHERE items.parent_id=%s\
        ORDER by is_parent DESC, depth DESC',
        [id, id]
    )

    # строим дерево меню
    def get_menu_tree(lst):
        level = {'name': lst[0].show_name, 'id': lst[0].parent_id}
        if len(lst) > 1:
            if lst[1].is_parent:
                level['children'] = []
                level['children'].append(get_menu_tree(lst[1:]))
            else:
                level['children'] = []
                for ls in lst[1:]:
                    level['children'].append({'name': ls.show_name, 'id': ls.id, 'children': {}})

        else:
            level['children'] = {}

        return level

    menu = get_menu_tree(items_list)
    name = Item.objects.get(id=id)

    data = {'menu': menu, 'name': name}
    return TemplateResponse(request,  "show.html", data)
