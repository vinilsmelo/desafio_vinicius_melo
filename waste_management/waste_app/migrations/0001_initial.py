# Generated by Django 5.0.1 on 2024-02-04 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WasteStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('volume_percentage', models.IntegerField(default=0)),
                ('collection_requested', models.BooleanField(default=False)),
                ('collection_confirmed', models.BooleanField(default=False)),
            ],
        ),
    ]
