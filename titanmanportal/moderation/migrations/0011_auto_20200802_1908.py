# Generated by Django 3.0.8 on 2020-08-02 19:08

from django.db import migrations, models
import moderation.models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0010_auto_20200802_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proof',
            name='proof_image',
            field=models.ImageField(blank=True, null=True, upload_to=moderation.models.Proof.proof_image_media_path, verbose_name='Фото/скрин'),
        ),
    ]