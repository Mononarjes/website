# Generated by Django 4.0 on 2022-01-18 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_remove_post_comments_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
