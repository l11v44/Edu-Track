

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published')], default='Draft', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='catalog.category')),
                ('students', models.ManyToManyField(blank=True, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('order', models.PositiveIntegerField(help_text='Order of the lesson in the course')),
                ('content', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='catalog.course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
