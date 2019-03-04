# Generated by Django 2.1.7 on 2019-03-03 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programdom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopsession',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='workshopsession',
            name='problems',
            field=models.ManyToManyField(blank=True, to='programdom.Problem'),
        ),
    ]
