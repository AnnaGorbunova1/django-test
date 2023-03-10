
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Пункты меню'
        verbose_name_plural = 'Пункты меню'


# таблица closure table для построения иерархической структуры
class ItemsTree(models.Model):
    parent = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemstree_parent', null=True, blank=True)
    child = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemstree_child')
    depth = models.IntegerField()


# триггер для заполнения таблицы ItemsTree при создании или изменении элемента Item
@receiver(post_save, sender=Item)
def create_closure(sender, instance, **kwargs):

    # delete old closures
    ItemsTree.objects.filter(child=instance).delete()

    # closure on self
    closure = ItemsTree.objects.create(parent=instance, child=instance, depth=0)
    closure.save()

    if instance.parent:
        # closure on nearest parent
        closure = ItemsTree.objects.create(parent=instance.parent, child=instance, depth=1)
        closure.save()

        # closure on other parents
        parents = ItemsTree.objects.filter(child=instance.parent, depth__gt=0)
        for p in parents:
            # print(p.parent_id.name, p.child_id.name, p.depth)
            closure = ItemsTree.objects.create(parent=p.parent, child=instance, depth=p.depth + 1)
            closure.save()

