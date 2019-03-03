# Generated by Django 2.1.7 on 2019-03-02 17:30

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mooshak_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.FileField(upload_to='')),
                ('options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programdom.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=2)),
                ('result_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('std_out', models.FileField(upload_to='')),
                ('std_err', models.FileField(upload_to='')),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='programdom.Submission')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, null=True)),
                ('problems', models.ManyToManyField(to='programdom.Problem')),
            ],
        ),
    ]
