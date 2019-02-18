import django_tables2 as tables

from programdom.models import Workshop


class WorkshopTable(tables.Table):

    class Meta:
        model = Workshop
        exclude = ['id']

    title = tables.LinkColumn()
    start_time = tables.DateTimeColumn()
    end_time = tables.DateTimeColumn()
