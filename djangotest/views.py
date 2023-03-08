from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import first
from django.template.response import TemplateResponse
from .models import *


def index(request):

    # получаем список элементов меню, у которых нет родителя
    # значит это наши названия меню
    roots = Item.objects.filter(parent_id__isnull=True)

    main_menu = []
    for rr in roots:
        it = Item.objects.get(name=rr.name)
        main_menu.append({'id': it.id, 'name': it.name})

    data = {'main_menu': main_menu}
    return TemplateResponse(request, "index.html", data)


def show(request, id):

    # дерево предков
    # и ближайшие потомки
    items_list = Item.objects.raw(
        'SELECT items.id id, itemparent.name as showname, tree.parent_id_id parent, tree.depth depth, 1 as isparent\
        FROM djangotest_item items\
        JOIN djangotest_itemstree tree\
        ON items.id=tree.child_id_id \
        JOIN djangotest_item itemparent\
        ON itemparent.id = tree.parent_id_id\
        WHERE items.id=%s\
        UNION\
        SELECT items.id id, items.name as showname, items.parent_id_id parent, 1 depth, 0 as isparent\
        FROM djangotest_item items\
        WHERE items.parent_id_id=%s\
        ORDER by isparent DESC, depth DESC',
        [id, id]
    )

    # строим дерево меню
    def get_menu_tree(lst):
        level = {'name': lst[0].showname, 'id': lst[0].parent}
        if len(lst) > 1:
            if lst[1].isparent:
                level['children'] = []
                level['children'].append(get_menu_tree(lst[1:]))
            else:
                level['children'] = []
                for ls in lst[1:]:
                    level['children'].append({'name': ls.showname, 'id': ls.id, 'children': {}})

        else:
            level['children'] = {}

        return level

    menu = get_menu_tree(items_list)

    print(menu)

    data = {'menu': menu}
    return TemplateResponse(request,  "show.html", data)
