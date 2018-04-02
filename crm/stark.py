from stark.server import stark
from crm.models import *
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import redirect, HttpResponse, render
from django.forms import ModelForm,widgets
import copy
from django.db.models import Q
import datetime
HttpResponse("ok")


class DepartmentConfig(stark.ModelStark):
    list_display = ["title", "code"]


class UserInfoConfig(stark.ModelStark):
    list_display = ["name", "email", "depart"]
    edit_link = ["name", ]


class CourseConfig(stark.ModelStark):
    list_display = ["name"]


class SchoolConfig(stark.ModelStark):
    list_display = ["title"]


class CustomerModelForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "date": widgets.TextInput(attrs={"type": "date"}),
            "last_consult_date": widgets.TextInput(attrs={"type": "date"}),
            "recv_date": widgets.TextInput(attrs={"type": "date"}),
        }


class CustomerConfig(stark.ModelStark):

    def display_gender(self, obj=None, is_head=False):
        if is_head:
            return "性别"
        else:
            return obj.get_gender_display()

    def display_state(self, obj=None, is_head=False):
        if is_head:
            return "状态"
        else:
            return obj.get_status_display()

    def display_genjin(self, obj=None, is_head=False):
        if is_head:
            return "跟进记录"
        else:
            tag = "<a href='/stark/crm/consultrecord/?customer=%s'>跟进记录</a>" % obj.pk
            return mark_safe(tag)

    def display_consult_course(self, obj=None, is_head=False):
        if is_head:
            return "咨询课程"
        else:
            params = copy.deepcopy(self.request.GET)
            course_list = obj.course.all()
            temp = []
            for course_obj in course_list:
                link = "<a class='customer-course' href='/stark/crm" \
                       "/customer/cancel_course/%s/%s?%s' style='padding:" \
                       "3px;border:1px solid #336699'>%s<span class='glyphicon glyphicon-remove'>" \
                       "</span></a>" % (obj.pk, course_obj.pk, params.urlencode(), course_obj.name)
                temp.append(link)
            s = " ".join(temp)
            return mark_safe(s)

    edit_link = ["name", ]
    list_display = ["name", display_gender, display_state, "consultant", display_consult_course, display_genjin]
    group_filter = [
        stark.FilterOption("gender", is_choice=True),
        stark.FilterOption("status", is_choice=True)
    ]
    model_form_class = CustomerModelForm
    def cancel_course(self, request, customer_id, course_id):
        # print("wowowowowowowowow")
        # print(request, customer_id, course_id)
        customer_obj = self.model.objects.get(pk=customer_id)

        customer_obj.course.remove(course_id)
        params = copy.deepcopy(request.GET)
        list_url = self.get_list_url()
        redirect_url = list_url + "?%s" % params.urlencode()
        return redirect(redirect_url)

    # 客户订单管理
    # 销售可以看自己的客户
    def personal_customer(self, request):
        login_consultant_id = 3

        customer_distrbute_list = CustomerDistrbute.objects.filter(consultant_id=login_consultant_id)

        return render(request, "consultant_cusomers.html", locals())

    # 过期客户抢单
    def take_customer(self, request, customer_id):
        login_user_id = 3  # 通过session获取当前登录用户的ID
        import datetime
        now = datetime.datetime.now()

        from django.db.models import Q

        # 三天未跟进 ：  now-最后跟进时间>3   15天未成单： now -接单日期>15
        q1 = Q(last_consult_date__lt=now - datetime.timedelta(days=3))
        q2 = Q(recv_date__lt=now - datetime.timedelta(days=15))

        rows = Customer.objects.filter(q1 | q2, pk=customer_id).update(consultant_id=login_user_id, recv_date=now,
                                                                       last_consult_date=now)
        if not rows:
            return HttpResponse("慢了！")

        #
        CustomerDistrbute.objects.create(customer_id=customer_id, consultant_id=login_user_id, date=now, status=1)

        return HttpResponse("抢单成功！")



    # 公共客户资源页面
    def public_customer(self, request):
        login_user_id = 2
        now = datetime.datetime.now()
        # 15天未成单
        q1 = Q(recv_date__lt=now-datetime.timedelta(days=15))
        # 三天未跟进
        q2 = Q(last_consult_date__lt=now-datetime.timedelta(days=3))

        customer_list = Customer.objects.filter(q1|q2, status=2).exclude(consultant_id=login_user_id)
        return render(request, "public_customer.html", locals())

    def get_extra_url(self):
        temp = [
            url(r'^cancel_course/(\d+)/(\d+)/', self.wrapper(self.cancel_course)),
            url(r'^public/', self.wrapper(self.public_customer)),
            url(r'^personal/', self.wrapper(self.personal_customer)),
            url(r'^qc/(\d+)/', self.wrapper(self.take_customer)),
        ]
        return temp


class ConsultRecordModelForm(ModelForm):
    class Meta:
        model = ConsultRecord
        fields = "__all__"
        widgets = {
            "date": widgets.TextInput(attrs={"type": "date"}),
            "last_consult_date": widgets.TextInput(attrs={"type": "date"}),
        }


class ConsultRecordConfig(stark.ModelStark):
    list_display = ["customer", "date"]
    group_filter = [
        stark.FilterOption("customer")
    ]
    group_tag_show = False
    # model_form_class = ConsultRecordModelForm


stark.site.register(Department, DepartmentConfig)
stark.site.register(UserInfo, UserInfoConfig)
stark.site.register(Course, CourseConfig)
stark.site.register(School, SchoolConfig)
stark.site.register(Customer, CustomerConfig)

stark.site.register(ClassList)
stark.site.register(ConsultRecord, ConsultRecordConfig)
stark.site.register(PaymentRecord)
stark.site.register(Student)
stark.site.register(CourseRecord)
stark.site.register(StudyRecord)
stark.site.register(CustomerDistrbute)
