# Generated by Django 4.1.8 on 2023-05-02 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryAI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('question', models.TextField(verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'История запросов к ИИ',
                'verbose_name_plural': 'История запросов к ИИ',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='HistoryDALLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('question', models.TextField(verbose_name='Запрос')),
                ('answer', models.JSONField(verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'История запросов к Dalle',
                'verbose_name_plural': 'История запросов к Dalle',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='HistoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('translation', models.TextField(verbose_name='Перевод')),
            ],
            options={
                'verbose_name': 'История запросов для перевода',
                'verbose_name_plural': 'История запросов для перевода',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='HistoryWhisper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('file_id', models.CharField(max_length=128, verbose_name='Id файла')),
                ('transcription', models.TextField(verbose_name='Аудиотранскрибция')),
            ],
            options={
                'verbose_name': 'История запросов к Whisper',
                'verbose_name_plural': 'История запросов к Whisper',
                'ordering': ('created_at',),
            },
        ),
    ]
