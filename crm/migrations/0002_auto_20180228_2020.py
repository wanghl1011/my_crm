# Generated by Django 2.0.2 on 2018-02-28 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDistrbute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='')),
                ('status', models.IntegerField(choices=[(1, '跟进状态'), (2, '已报名'), (3, '三天未跟进'), (4, '15天未成单')], default=1)),
                ('memo', models.CharField(max_length=255)),
                ('consultant', models.ForeignKey(limit_choices_to={'depart_id': 1001}, on_delete=django.db.models.deletion.CASCADE, to='crm.UserInfo', verbose_name='课程顾问')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='recv_date',
            field=models.DateField(null=True, verbose_name='当前课程顾问的接单日期'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(limit_choices_to={'depart_id': 1001}, on_delete=django.db.models.deletion.CASCADE, related_name='consultanter', to='crm.UserInfo', verbose_name='课程顾问'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(verbose_name='咨询日期'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_consult_date',
            field=models.DateField(verbose_name='最后跟进日期'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='qq',
            field=models.CharField(help_text='QQ号必须唯一', max_length=64, unique=True, verbose_name='QQ'),
        ),
        migrations.AddField(
            model_name='customerdistrbute',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='crm.Customer'),
        ),
    ]
