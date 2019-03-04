import django_tables2 as tables

from programdom.models import WorkshopSession


class WorkshopTable(tables.Table):

    class Meta:
        model = WorkshopSession
        fields = ['title', 'active']

    active = tables.BooleanColumn()
    title = tables.LinkColumn()