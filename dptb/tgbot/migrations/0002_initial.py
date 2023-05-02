# Generated by Django 4.1.8 on 2023-05-02 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tgbot', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='historywhisper',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_whisper', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historytranslation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_translation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historydalle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_dalle', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historyai',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_ai', to=settings.AUTH_USER_MODEL),
        ),
    ]