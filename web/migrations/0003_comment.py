# Generated by Django 3.0.5 on 2020-05-18 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20200513_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('comment', models.TextField()),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Publication')),
            ],
        ),
    ]
