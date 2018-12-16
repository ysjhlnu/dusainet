# Generated by Django 2.0.6 on 2018-12-15 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vlog', '0002_auto_20181215_2050'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0022_auto_20181213_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='VlogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='正文')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vlog_comments', to='vlog.Vlog', verbose_name='文章')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='comments.VlogComment', verbose_name='父级')),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vlog_comments_reply_to', to=settings.AUTH_USER_MODEL, verbose_name='评论给')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vlog_comments_user', to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
