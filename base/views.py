import os

from django.shortcuts import render, redirect

from EasyTest.settings import STATICFILES_DIRS
from base import models
from base.models import Project, Sign, Environment, Interface, Case, Plan, Report, Photo, CategoryPhoto
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.core import serializers
from base.dataObject.dataObjs import contentObj
from lib.execute import Execute
import time
import json
import numpy as np

# Create your views here.


# 项目增删改查
from lib.timeload import TimeLoad


def project_index(request):
    prj_list = Project.objects.all()
    return render(request, "base/project/index.html", {"prj_list": prj_list})


def project_add(request):
    if request.method == 'POST':
        prj_name = request.POST['prj_name']
        name_same = Project.objects.filter(prj_name=prj_name)
        if name_same:
            messages.error(request, "项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign']
            print("sign_id:", sign_id)
            sign = Sign.objects.get(sign_id=sign_id)
            print("sign:", sign)
            prj = Project(prj_name=prj_name, description=description, sign=sign)
            prj.save()
            return HttpResponseRedirect("/base/project/")
    sign_list = Sign.objects.all()
    return render(request, "base/project/add.html", {"sign_list": sign_list})


def project_update(request):
    if request.method == 'POST':
        prj_id = request.POST['prj_id']
        prj_name = request.POST['prj_name']
        name_exit = Project.objects.filter(prj_name=prj_name).exclude(prj_id=prj_id)
        if name_exit:
            # messages.error(request, "项目已存在")
            return HttpResponse("项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign_id']
            sign = Sign.objects.get(sign_id=sign_id)
            Project.objects.filter(prj_id=prj_id).update(prj_name=prj_name, description=description, sign=sign)
            return HttpResponseRedirect("/base/project/")
    prj_id = request.GET['prj_id']
    prj = Project.objects.get(prj_id=prj_id)
    sign_list = Sign.objects.all()
    return render(request, "base/project/update.html", {"prj": prj, "sign_list": sign_list})


def project_delete(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        Project.objects.filter(prj_id=prj_id).delete()
        return HttpResponseRedirect("base/project/")


# 加密方式增删改查
def sign_index(request):
    sign_list = Sign.objects.all()
    return render(request, "system/sign_index.html", {"sign_list": sign_list})


def sign_add(request):
    if request.method == 'POST':
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        sign = Sign(sign_name=sign_name, description=description)
        sign.save()
        return HttpResponseRedirect("/base/sign/")
    return render(request, "system/sign_add.html")


# 更新加密方式
def sign_update(request):
    if request.method == 'POST':
        sign_id = request.POST['sign_id']
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        Sign.objects.filter(sign_id=sign_id).update(sign_name=sign_name, description=description)
        return HttpResponseRedirect("/base/sign/")
    sign_id = request.GET['sign_id']
    sign = Sign.objects.get(sign_id=sign_id)
    return render(request, "system/sign_update.html", {"sign": sign})


# 删除加密方式
def sign_delete(request):
    if request.method == 'GET':
        sign_id = request.GET['sign_id']
        print("****", sign_id)
        Sign.objects.filter(sign_id=sign_id).delete()
        return HttpResponseRedirect("/base/sign/")


# 图片显示页
def photo_index(request):
    photo_list = Photo.objects.all()
    photo_category_list = CategoryPhoto.objects.all()
    print("图片列表:", photo_list, "图片类目:", photo_category_list)
    return render(request, "photo/photo_index.html",
                  {"photo_list": photo_list, "photo_category_list": photo_category_list})


# 图片上传页
def photo_upload(request):
    if request.method == 'POST':
        pic_name = request.POST['photo_name']
        name_same = Photo.objects.filter(photo_name=pic_name)
        if name_same:
            messages.error(request, "图片名称已存在")
        else:
            pic = request.FILES.get('photo', '')
            description = request.POST['description']
            click_num = 0
            # content_time = TimeLoad.local_sys_time()
            cate_id = request.POST['pcl']
            print("cate_id:", cate_id)
            category = CategoryPhoto.objects.get(cate_id=cate_id)
            print("图片参数:", pic, description, category)
            # 入库操作
            photo = Photo(photo_name=pic_name, description=description, photo=pic, click=click_num,
                          category_photo=category)
            photo.save()
            # return HttpResponse("上传成功!!!")
            return HttpResponseRedirect("/base/photo")

    photo_list = Photo.objects.all()
    print("********", photo_list)
    # 先获取类目列表
    photo_category_list = CategoryPhoto.objects.all()

    print("图片列表:", photo_list, "图片类目:", photo_category_list)
    return render(request, "photo/photo_index.html",
                  {"photo_list": photo_list, "photo_category_list": photo_category_list})


def photo_download(request):
    # if request.method == 'POST':
    # 获取请求参数（图片存储位置） imgs/5566.jpg
    photo = request.GET.get('photo', '')
    # photo = request.FILES.get('photo', '')
    print("sssss", photo)
    # 获取图片文件名5566.jpg ; rindex 为字符 '/' 在 photo 中最后出现的位置索引；例如
    txt = "imgs/5566.jpg"
    x = txt.rindex("/")
    print(txt[x + 1:])  # 输出结果为 5566.jpg
    filename = photo[photo.rindex('/') + 1:]
    print("filename", filename)
    # 开启一个流
    # path = os.path.join(os.getcwd(), 'media', photo.replace('/', '\\'))
    path = os.path.join(os.getcwd(), 'static', photo)
    print("图片路径:", path)

    with open(path, 'rb') as fr:
        response = HttpResponse(fr.read())
        response['Content-Type'] = 'image/png'
        response['Content-Disposition'] = 'attachment;filename=' + filename
    return response


def photo_update(request):
    if request.method == 'POST':
        pic_id = request.POST['photo_id']
        pic_name = request.POST['photo_name']
        description = request.POST['description']
        # 入库操作
        Photo.objects.filter(photo_id=pic_id).update(photo_name=pic_name, description=description)
        return HttpResponseRedirect("/base/photo/")
    pic_id = request.GET['photo_id']
    photo = Photo.objects.get(photo_id=pic_id)
    return render(request, "photo/photo_update.html", {"photo": photo})


def photo_delete(request):
    if request.method == 'GET':
        pic_id = request.GET['photo_id']
        Photo.objects.filter(photo_id=pic_id).delete()
        return HttpResponseRedirect("/base/photo/")

def photo_filter(request):
    if request.method == 'GET':
        cate_id = request.POST['pcl']
        print("cate_id:", cate_id)
        category = CategoryPhoto.objects.get(cate_id=cate_id)
        c_list = Photo.objects.filter(category_photo=category)
        return render(request, "photo/category/photo_category_index.html", {"photo_category_list": c_list})


# 图片类目管理页面
def photo_category_index(request):
    photo_category_list = CategoryPhoto.objects.all()
    return render(request, "photo/category/photo_category_index.html", {"photo_category_list": photo_category_list})


def photo_category_add(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        description = request.POST['description']
        cp = CategoryPhoto(category_name=category_name, description=description)
        cp.save()
        return HttpResponseRedirect("/base/photo_category/")
    photo_category_list = Project.objects.all()
    return render(request, "photo/category/photo_category_index.html", {"photo_category_list": photo_category_list})


def photo_category_update(request):
    if request.method == 'POST':
        category_id = request.POST['cate_id']
        category_name = request.POST['category_name']
        description = request.POST['description']
        CategoryPhoto.objects.filter(cate_id=category_id).update(category_name=category_name, description=description)
        return HttpResponseRedirect("/base/photo_category/")
    category_id = request.GET['cate_id']
    photo_category_list = CategoryPhoto.objects.get(cate_id=category_id)
    return render(request, "photo/category/photo_category_update.html", {"photo_category_list": photo_category_list})


def photo_category_delete(request):
    if request.method == 'GET':
        category_id = request.GET['cate_id']
        CategoryPhoto.objects.filter(cate_id=category_id).delete()
        return HttpResponseRedirect("/base/photo_category/")


def env_index(request):
    env_list = Environment.objects.all()
    return render(request, "base/env/index.html", {"env_list": env_list})


def env_add(request):
    if request.method == 'POST':
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        env = Environment(env_name=env_name, url=url, project=project,
                          private_key=private_key, description=description)
        env.save()
        return HttpResponseRedirect("/base/env/")
    prj_list = Project.objects.all()
    return render(request, "base/env/add.html", {"prj_list": prj_list})


# 测试环境更新
def env_update(request):
    if request.method == 'POST':
        env_id = request.POST['env_id']
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        Environment.objects.filter(env_id=env_id).update(env_name=env_name, url=url, project=project,
                                                         private_key=private_key, description=description)
        return HttpResponseRedirect("/base/env/")
    env_id = request.GET['env_id']
    env = Environment.objects.get(env_id=env_id)
    prj_list = Project.objects.all()
    return render(request, "base/env/update.html", {"env": env, "prj_list": prj_list})


def env_delete(request):
    if request.method == 'GET':
        env_id = request.GET['env_id']
        Environment.objects.filter(env_id=env_id).delete()
        return HttpResponseRedirect("/base/env/")


# 接口增删改查
def interface_index(request):
    if_list = Interface.objects.all()
    return render(request, "base/interface/index.html", {"if_list": if_list})


def interface_add(request):
    if request.method == 'POST':
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data = request.POST['request_header_data']
        request_body_data = request.POST['request_body_data']
        response_header_data = request.POST['response_header_data']
        response_body_data = request.POST['response_body_data']
        interface = Interface(if_name=if_name, url=url, project=project, method=method, data_type=data_type,
                              is_sign=is_sign, description=description, request_header_param=request_header_data,
                              request_body_param=request_body_data, response_header_param=response_header_data,
                              response_body_param=response_body_data)
        interface.save()
        return HttpResponseRedirect("/base/interface/")
    prj_list = Project.objects.all()
    return render(request, "base/interface/add.html", {"prj_list": prj_list})


# 测试接口更新
def interface_update(request):
    if request.method == 'POST':
        if_id = request.POST['if_id']
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data1 = request.POST['request_header_data']
        request_body_data1 = request.POST['request_body_data']
        response_header_data1 = request.POST['response_header_data']
        response_body_data1 = request.POST['response_body_data']

        Interface.objects.filter(if_id=if_id).update(if_name=if_name, url=url, project=project, method=method,
                                                     data_type=data_type,
                                                     is_sign=is_sign, description=description,
                                                     request_header_param=request_header_data1,
                                                     request_body_param=request_body_data1,
                                                     response_header_param=response_header_data1,
                                                     response_body_param=response_body_data1)

        return HttpResponseRedirect("/base/interface/")
    if_id = request.GET['if_id']
    it = Interface.objects.get(if_id=if_id)
    request_header_data = json.loads(it.request_header_param)
    request_body_data = json.loads(it.request_body_param)
    response_header_data = json.loads(it.response_header_param)
    response_body_data = json.loads(it.response_body_param)
    request_header = np.array(request_header_data)
    request_body = np.array(request_body_data)
    response_header = np.array(response_header_data)
    response_body = np.array(response_body_data)
    request_header_list = request_header.tolist()
    request_body_list = request_body.tolist()
    response_header_list = response_header.tolist()
    response_body_list = response_body.tolist()
    request_header_dict = {}
    request_body_dict = {}
    response_header_dict = {}
    response_body_dict = {}

    for r in request_header_list:
        request_header_dict[r["var_name"]] = r["var_remark"]

    for r in request_body_list:
        request_body_dict[r["var_name"]] = r["var_remark"]

    for r in response_header_list:
        response_header_dict[r["var_name"]] = r["var_remark"]

    for r in response_body_list:
        response_body_dict[r["var_name"]] = r["var_remark"]

    prj_list = Project.objects.all()

    return render(request, "base/interface/update.html",
                  {"it": it, "prj_list": prj_list, "request_header_dict": request_header_dict,
                   "request_body_dict": request_body_dict, "response_header_dict": response_header_dict,
                   "response_body_dict": response_body_dict})


# 接口删除
def interface_delete(request):
    if request.method == 'GET':
        if_id = request.GET['if_id']
        Interface.objects.filter(if_id=if_id).delete()
        return HttpResponseRedirect("base/interface/")


# 用例增删改查
def case_index(request):
    case_list = Case.objects.all()
    return render(request, "base/case/index.html", {"case_list": case_list})


def case_add(request):
    if request.method == 'POST':
        case_name = request.POST['case_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        description = request.POST['description']
        content = request.POST['content']
        case = Case(case_name=case_name, project=project, description=description, content=content)
        case.save()
        return HttpResponseRedirect("/base/case/")
    prj_list = Project.objects.all()
    return render(request, "base/case/add.html", {"prj_list": prj_list})


def case_update(request):
    if request.method == 'POST':
        case_id = request.POST['case_id']
        case_name = request.POST['case_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        description = request.POST['description']
        content = request.POST['content']
        Case.objects.filter(case_id=case_id).update(case_name=case_name, project=project, content=content,
                                                    description=description)
        return HttpResponseRedirect("/base/case/")
    case_id = request.GET['case_id']
    case = Case.objects.get(case_id=case_id)
    content_data = json.loads(case.content)
    content_data_array = np.array(content_data)
    content_data_List = content_data_array.tolist()
    content_list = []

    for c in content_data_List:
        contentObj.if_id = c["if_id"]
        contentObj.if_name = c["if_name"]
        header_dict = {}
        header_dict = c["header"]
        for key in header_dict:
            print(key)
            contentObj.header[key] = header_dict[key]
            print(header_dict[key])

        body_dict = {}
        body_dict = c["body"]
        for key in body_dict:
            print(key)
            contentObj.body[key] = body_dict[key]
            print(body_dict[key])

        extrace_dict = c["extract"]
        for key in extrace_dict:
            print(key)
            contentObj.extract[key] = extrace_dict[key]
            print(extrace_dict[key])

        validate = np.array(c["validators"])
        validate_list = validate.tolist()
        validate_dict = {}
        for v in validate_list:
            validate_dict[v["check"]] = v["expect"]

        contentObj.validator = validate_dict
        content_list.append(contentObj)

    prj_list = Project.objects.all()
    return render(request, "base/case/update.html", {"case": case, "prj_list": prj_list, "content_list": content_list})


def case_delete(request):
    if request.method == 'GET':
        case_id = request.GET['case_id']
        Case.objects.filter(case_id=case_id).delete()
        return HttpResponseRedirect("base/case/")


def case_run(request):
    if request.method == 'POST':
        case_id = request.POST['case_id']
        env_id = request.POST['env_id']
        execute = Execute(case_id, env_id)
        case_result = execute.run_case()
        return JsonResponse(case_result)


# 计划增删改查
def plan_index(request):
    plan_list = Plan.objects.all()
    return render(request, "base/plan/index.html", {"plan_list": plan_list})


def plan_add(request):
    if request.method == 'POST':
        plan_name = request.POST['plan_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        env_id = request.POST['env_id']
        environment = Environment.objects.get(env_id=env_id)
        description = request.POST['description']
        content = request.POST.getlist("case_id")
        plan = Plan(plan_name=plan_name, project=project, environment=environment, description=description,
                    content=content)
        plan.save()
        return HttpResponseRedirect("/base/plan/")
    prj_list = Project.objects.all()
    return render(request, "base/plan/add.html", {"prj_list": prj_list})


def plan_update(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        plan_name = request.POST['plan_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        env_id = request.POST['env_id']
        environment = Environment.objects.get(env_id=env_id)
        content = request.POST.getlist("case_id")
        description = request.POST['description']
        Plan.objects.filter(plan_id=plan_id).update(plan_name=plan_name, environment=environment, project=project,
                                                    description=description, content=content)
        return HttpResponseRedirect("/base/env/")
    plan_id = request.GET['plan_id']
    plan = Plan.objects.get(plan_id=plan_id)
    content_list = eval(plan.content)
    prj_list = Project.objects.all()
    return render(request, "base/plan/update.html", {"plan": plan, "prj_list": prj_list, "content_list": content_list})


def plan_delete(request):
    if request.method == 'GET':
        plan_id = request.GET['plan_id']
        Plan.objects.filter(plan_id=plan_id).delete()
        return HttpResponseRedirect("base/plan/")


def plan_run(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        plan = Plan.objects.get(plan_id=plan_id)
        env_id = plan.environment.env_id
        case_id_list = eval(plan.content)
        case_num = len(case_id_list)
        content = []
        pass_num = 0
        fail_num = 0
        error_num = 0
        for case_id in case_id_list:
            execute = Execute(case_id, env_id)
            case_result = execute.run_case()
            content.append(case_result)
            if case_result["result"] == "pass":
                pass_num += 1
            if case_result["result"] == "fail":
                fail_num += 1
            if case_result["result"] == "error":
                error_num += 1
        report_name = plan.plan_name + "-" + time.strftime("%Y%m%d%H%M%S")
        if Report.objects.filter(plan=plan):
            Report.objects.filter(plan=plan).update(report_name=report_name, content=content, case_num=case_num,
                                                    pass_num=pass_num, fail_num=fail_num, error_num=error_num)
        else:
            report = Report(plan=plan, report_name=report_name, content=content, case_num=case_num,
                            pass_num=pass_num, fail_num=fail_num, error_num=error_num)
            report.save()
        return HttpResponse(plan.plan_name + " 执行成功！")


def report_index(request):
    plan_id = request.GET['plan_id']
    report = Report.objects.get(plan_id=plan_id)
    report_content = eval(report.content)
    return render(request, "report.html", {"report": report, "report_content": report_content})


def findata(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        get_type = request.GET["type"]
        if get_type == "get_all_if_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 返回字典列表
            if_list = Interface.objects.filter(project=prj_id).all().values()
            # list(if_list)将QuerySet转换成list
            return JsonResponse(list(if_list), safe=False)
        if get_type == "get_if_by_if_id":
            if_id = request.GET["if_id"]
            # 查询并将结果转换为json
            interface = Interface.objects.filter(if_id=if_id).values()
            return JsonResponse(list(interface), safe=False)
        if get_type == "get_env_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Environment.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)
        if get_type == "get_all_case_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Case.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)
