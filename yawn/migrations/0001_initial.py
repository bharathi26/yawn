# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-22 20:00
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.functions
import yawn.utilities.cron


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(
                    choices=[('running', 'running'), ('succeeded', 'succeeded'), ('failed', 'failed'),
                             ('killed', 'killed'), ('lost', 'lost')], default='running')),
                ('start_timestamp', models.DateTimeField(default=django.db.models.functions.Now)),
                ('stop_timestamp', models.DateTimeField(null=True)),
                ('exit_code', models.IntegerField(null=True)),
                ('stdout', models.TextField(blank=True, default='')),
                ('stderr', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(allow_unicode=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_time', models.DateTimeField()),
                ('scheduled_time', models.DateTimeField(null=True)),
                ('status',
                 models.TextField(choices=[('running', 'running'), ('succeeded', 'succeeded'), ('failed', 'failed')],
                                  default='running')),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(
                    choices=[('waiting', 'waiting'), ('queued', 'queued'), ('running', 'running'),
                             ('succeeded', 'succeeded'), ('failed', 'failed'), ('upstream_failed', 'upstream_failed')],
                    default='waiting')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Run')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(allow_unicode=True, db_index=False)),
                ('command', models.TextField()),
                ('max_retries', models.IntegerField(default=0)),
                ('timeout', models.IntegerField(null=True)),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Queue')),
                ('upstream', models.ManyToManyField(blank=True, related_name='downstream', to='yawn.Template')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('status', models.TextField(choices=[('active', 'active'), ('exited', 'exited'), ('lost', 'lost')],
                                            default='active')),
                ('start_timestamp', models.DateTimeField(default=django.db.models.functions.Now)),
                ('last_heartbeat', models.DateTimeField(default=django.db.models.functions.Now)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(editable=False)),
                ('schedule_active', models.BooleanField(default=False)),
                ('schedule', models.TextField(null=True, validators=[yawn.utilities.cron.cron_validator])),
                ('next_run', models.DateTimeField(null=True)),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(allow_unicode=True, unique=True)),
                ('current_version',
                 models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='is_current',
                                      to='yawn.Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='workflow',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.WorkflowName'),
        ),
        migrations.AddField(
            model_name='template',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='yawn.Workflow'),
        ),
        migrations.AddField(
            model_name='task',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Template'),
        ),
        migrations.AddField(
            model_name='run',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Workflow'),
        ),
        migrations.AddField(
            model_name='message',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Queue'),
        ),
        migrations.AddField(
            model_name='message',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Task'),
        ),
        migrations.AddField(
            model_name='execution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Task'),
        ),
        migrations.AddField(
            model_name='execution',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='yawn.Worker'),
        ),
        migrations.AlterUniqueTogether(
            name='workflow',
            unique_together=set([('name', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('workflow', 'name')]),
        ),
    ]
