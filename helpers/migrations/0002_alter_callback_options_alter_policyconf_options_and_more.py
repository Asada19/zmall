# Generated by Django 4.1.4 on 2023-01-17 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='callback',
            options={'verbose_name': 'Обратная связь', 'verbose_name_plural': 'Обратная связь'},
        ),
        migrations.AlterModelOptions(
            name='policyconf',
            options={'verbose_name': 'Политика конфиденциальности', 'verbose_name_plural': 'Политика конфиденциальности'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопрос'},
        ),
        migrations.AlterModelOptions(
            name='questioncategory',
            options={'verbose_name': 'Категория вопросов', 'verbose_name_plural': 'Категория вопросов'},
        ),
        migrations.AlterField(
            model_name='questioncategory',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
