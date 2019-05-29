# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-28 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Planner', '0006_auto_20190528_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Planner.User')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='apps/Planner/static/images/default.jpg', upload_to='apps/Planner/static/images/'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post_commented',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Planner.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Planner.User'),
        ),
    ]