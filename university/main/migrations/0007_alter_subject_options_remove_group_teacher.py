# Generated by Django 4.2.5 on 2024-04-16 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_professor_middle_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'дисциплину', 'verbose_name_plural': 'Дисциплины'},
        ),
        migrations.RemoveField(
            model_name='group',
            name='teacher',
        ),
    ]
