# Generated by Django 4.0.6 on 2022-08-28 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_comment_updated_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
