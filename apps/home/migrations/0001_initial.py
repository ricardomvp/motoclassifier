# Generated by Django 3.1.2 on 2020-11-05 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('bucket_url', models.TextField()),
                ('cathegory', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]