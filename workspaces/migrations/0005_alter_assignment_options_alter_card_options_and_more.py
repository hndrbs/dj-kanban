# Generated by Django 4.0.2 on 2022-03-01 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0004_alter_board_options_remove_board_board_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['-updated_at', '-created_at']},
        ),
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-updated_at', '-created_at']},
        ),
        migrations.AlterModelOptions(
            name='workspace',
            options={'ordering': ['-updated_at', '-created_at']},
        ),
    ]
