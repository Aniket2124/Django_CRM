# Generated by Django 4.1.2 on 2022-10-22 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_category_organizations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='organizations',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]
