# Generated by Django 4.2.5 on 2023-10-02 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0002_portfolio_alter_student_major_student_portfolio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('portfolio', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='portfolio_app.portfolio')),
            ],
        ),
    ]