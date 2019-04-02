import django_tables2 as tables

from programdom.models import Workshop


class WorkshopTable(tables.Table):

    class Meta:
        model = Workshop
        fields = ['title', 'active']

    active = tables.BooleanColumn()
    title = tables.LinkColumn()