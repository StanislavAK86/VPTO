# Generated by Django 4.2 on 2024-11-04 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_alter_answer_options_alter_choice_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='group',
            new_name='group_id',
        ),
    ]
