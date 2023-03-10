# Generated by Django 4.1.4 on 2023-01-13 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Callback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(choices=[('Жалоба', 'Жалоба'), ('Предложение', 'Предложение')], default='Жалоба', max_length=30)),
                ('text', models.TextField(max_length=2000)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('checked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PolicyConf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Политика конфиденциальности', max_length=255)),
                ('text', models.TextField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=3000)),
            ],
            options={
                'verbose_name': 'Категория вопросов',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('answer', models.TextField(max_length=3000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='helpers.questioncategory')),
            ],
            options={
                'verbose_name': 'Вопрос',
            },
        ),
    ]
