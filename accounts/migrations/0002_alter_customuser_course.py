from django.db import migrations, models


def replace_null_courses(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')
    CustomUser.objects.filter(course__isnull=True).update(course='')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(replace_null_courses, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='customuser',
            name='course',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
