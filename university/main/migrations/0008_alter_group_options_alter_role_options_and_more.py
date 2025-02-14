# Generated by Django 4.2.5 on 2024-05-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_subject_options_remove_group_teacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'группу', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'роль', 'verbose_name_plural': 'Роли'},
        ),
        migrations.AlterModelOptions(
            name='score',
            options={'verbose_name': 'оценки', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterField(
            model_name='professor',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
    ]
