import unittest
from django.urls import reverse
from django.forms.models import ModelChoiceField
from django import template

from django.db.models.fields.related import ForeignKey,ManyToManyField,OneToOneField
from django.db.models.fields.reverse_related import ManyToOneRel

# 必须叫register
register = template.Library()
# 引入装饰器，filter就是过滤器
@register.filter
def cheng(a,b):
    # 参数a就代表被渲染的模版变量，b就代表冒号后跟着的参数
    return a*b

# 参数是模版文件名，会把返回值作为参数传到模版里，模版中利用模版语法进行渲染
@register.inclusion_tag("form_show.html")
def get_form_info(config, form):
    form_info = []
    for field in form:
        # print(field,"%r"%field)
        if isinstance(field.field, ModelChoiceField):
            # 当前字段对象对应关联的model类
            field_model = field.field.queryset.model
            # 对应的model类的app名
            _app_label = field_model._meta.app_label
            # 对应的model类的名字
            _model_name = field_model._meta.model_name

            # print(field)
            # print(field.name)            print(config.model._meta)
            print(">>>>>>>>>>>>>>>>>>>>")
            print(field.name)
            print(config.model._meta)
            obj = config.model._meta.get_field(field.name)
            # print(isinstance(obj,ForeignKey))
            # print(obj)
            # print(config.model._meta.get_field(field.name).related_name)
            print("<<<<<<<<<<<<<<<<<<<<")

            # 当前字段对应的related_name值和对应的表名
            relatedNmae = config.model._meta.get_field(field.name).related_name
            modelName = config.model._meta.model_name

            pop_up_id = field.auto_id
            name = "stark:%s_%s_add" % (_app_label, _model_name)
            _url = reverse(name)
            fina_url = "%s?pop_up_id=%s&rn=%s&mn=%s" % (_url, pop_up_id,relatedNmae,modelName)
            form_info.append({"form": field, "is_pop_up": True, "url": fina_url})
        else:
            form_info.append({"form": field, "is_pop_up": False})
    # 返回的时候要用这种字典的形式，key必须是模版中定义的变量
    return {"form_info":form_info}