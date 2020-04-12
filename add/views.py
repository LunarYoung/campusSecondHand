from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.core.mail import send_mail, send_mass_mail
import random
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image,ImageDraw,ImageFont


from add import models
from add.models import upthing
from .forms import MyForm, upthingform, upneedform




def paginator_view(request):
    thing_list = models.upthing.objects.all()

    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(thing_list, 2)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            things = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            things = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            things = paginator.page(paginator.num_pages)

    template_view = 'thingStore.html'
    return render(request, template_view, {'things':things})



def index(request):
     thing_list = models.upthing.objects.order_by("data")
     return render(request, 'index.html', {"thing_list": thing_list})


def logout(request):
    request.session.flush()
    return redirect('/')


def up(request):
    eroor = "请从新检查输入框"
    username = request.session.get('username', '')
    if not username:
        return redirect("/login/")
    form =upthingform(request.POST)
    if request.method == "POST" and form.is_valid():
            pic = request.FILES.get('pic')
            pic1 = request.FILES.get('pic1')
            if not pic or not pic1:
                return render(request, 'sellUpload.html', {"eroor": eroor})
            link = request.POST.get('link')
            # username = request.session.get('username', '')
            price = request.POST.get('price')
            type = request.POST.get('type')
            dtail = request.POST.get('detail')
            new_thing = models.upthing.objects.create()
            new_thing.Thing_own = username
            new_thing.image = pic
            new_thing.image1 = pic1
            new_thing.link = link
            new_thing.price = price
            new_thing.type = type
            new_thing.dtail = dtail
            new_thing.save()
            secces = "上传成功"
            return render(request, 'sellUpload.html', {'secces': secces})

    return render(request, 'sellUpload.html', )


def mything(request):
    username = request.session.get('username', '')
    if not username:
        return redirect("/login/")
    else:
        own_thing = models.upthing.objects.filter(Thing_own=username)
    if request.method == 'POST':
        thing_id = request.POST.get('thing-id')
        thing = models.upthing.objects.get(id=thing_id)
        thing.delete()


    return render(request, 'mythingself.html', {"a":own_thing} )



def myupneed(request):
    username = request.session.get('username', '')
    if not username:
        return redirect("/login/")
    else:
        own_need = models.upneed.objects.filter(upName=username)
    if request.method == 'POST':
        up_id = request.POST.get('up-id')
        thing = models.upneed.objects.get(id=up_id)
        thing.delete()

    return render(request, 'myQiugou.html', {"a": own_need})



def Thing_detail(request, pk):
    post = get_object_or_404(upthing, pk=pk)
    thing_id=int(pk)
    thing_All=models.upthing.objects.get(id=thing_id)
    print(post)
    print("----------")
    return render(request, 'thingDetail.html', {"thing_All": thing_All})


def login(request):
    if request.method == "GET":
        yanzheng = random.randint(1000, 9999)
        a =str(yanzheng)
        font = ImageFont.truetype('bahnschrift.ttf', 24)  # 定义字体，这是本地自己下载的
        img = Image.new('RGB', (56, 25), (255, 255, 255))  # 新建长宽300像素，背景色为（255,180,0）的画布对象
        draw = ImageDraw.Draw(img)  # 新建画布绘画对象
        draw.text((1, 1), a , (0, 0, 255), font=font)  # 在新建的对象 上坐标（50,50）处开始画出红色文本
        # 左上角为画布坐标（0,0）点
        img.save('media/yzm.png')
        Yzm = models.Yzm.objects.create()
        Yzm.yzm = yanzheng
        Yzm.save()
        return render(request, 'login.html', {'yanzheng': yanzheng})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        yam = request.POST.get('yzm')
        yanzheng = random.randint(1000, 9999)
        a = str(yanzheng)
        font = ImageFont.truetype('bahnschrift.ttf', 24)  # 定义字体，这是本地自己下载的
        img = Image.new('RGB', (56, 25), (255, 255, 255))  # 新建长宽300像素，背景色为（255,180,0）的画布对象
        draw = ImageDraw.Draw(img)  # 新建画布绘画对象
        draw.text((1, 1), a, (0, 0, 255), font=font)  # 在新建的对象 上坐标（50,50）处开始画出红色文本
        # 左上角为画布坐标（0,0）点
        img.save('media/yzm.png')
        Yzm = models.Yzm.objects.create()
        Yzm.yzm = yanzheng
        Yzm.save()
        data1 = ["用户名或密码有误"]
        secces = '登陆成功'
        if username and password and yam:
            try:
                user = models.User.objects.get(name=username)
                yanzheng = models.Yzm.objects.get(yzm=yam)
                print(yanzheng)
                if user.password == password :
                    request.session['username'] = username
                    return redirect("/")
                    # return render(request, 'login.html', {'secces': secces} )
                else:
                    return render(request, 'login.html', {'data': data1})
            except:
                return render(request, 'login.html', {'data': data1})
        else:
            return render(request, 'login.html', {'data': data1})

def register(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        data = '注册成功'
        if form.is_valid():
            username = request.POST.get('username')
            try:
                user = models.User.objects.get(name=username)
                re1 = '用户已存在'
                if user.name == username :
                    return render(request ,'register.html', {'re1': re1})
            except:
                password = request.POST.get('password')
                email = request.POST.get('email')
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password
                new_user.email = email
                new_user.save()
                request.session['username'] = username
                return redirect("/")

                #return render(request, 'register.html', {'data': data})
        else:
            error_date = '账户，密码需六位以上，'
            return render(request, 'register.html', {'error': error_date})


    return render(request, 'register.html')
def edict(request):
    if request.method == "POST":
        new_email = request.POST.get('c_email')
        new_password = request.POST.get('c_password')
        username = request.session.get('username', '')
        user = models.User.objects.get(name=username)
        secces = "修改成功 "
        if new_password and new_email:
            user.password = new_password
            user.email = new_email
            user.save()
            return render(request, 'edict.html', {"secces":secces})
        if new_password and not new_email:
            user.password = new_password
            user.save()
            return render(request, 'edict.html', {"secces":secces})
        if not new_password and new_email:
            user.email = new_email
            user.save()
            return render(request, 'edict.html', {"secces":secces})
        if not new_password and not new_email:
            error = "请不要提交空表单"
            return render(request, 'edict.html', {"error":error})

    return render(request, 'edict.html')


# def re_email(request):
#     if request.method =="POST":
#
#         m = random.randrange(1000, 9999)
#         v = str(m)
#
#         send_mail('校园二手交易网站验证码', v,
#                   settings.EMAIL_FROM,
#                   ['2912344081@qq.com']
#                   )
#         secces = "发送成功|"
#
#
#
#
#         return render(request, "email.html", {"secces": secces})
#
#
#     return render(request, "email.html")



def re_email(request):
    if request.method =="POST":
        email_r = request.POST.get('email')
        re_email_code = request.POST.get('re_email')

        if not re_email_code and email_r:
            try:
                m = random.randrange(1000, 9999)
                v = str(m)
                email1 = email_r.split(',')
                send_mail('校园二手交易网站验证码', v,
                          settings.EMAIL_FROM,
                            email1
                          )
                secces_1 = "发送成功|"
                secces_2 = email_r
                secces_3 =secces_1 + secces_2
                secces = secces_3.split('|')
                user = models.User.objects.get(email=email_r)
                user.i_code = v
                user.save()
                return render(request, "email.html", {"secces": secces})
            except:
                not_man = "邮箱有错"
                return render(request, "email.html", {"not_man": not_man})

        if re_email_code and email_r:
            try:
                user = models.User.objects.get(email=email_r)
                if user.i_code == re_email_code:
                    request.session['username'] = user.name
                    return redirect("/")
            except:
                t_error = "邮箱或密码错误"
                return render(request, "email.html", {"t_error": t_error})

        else:
            t_tip = "请填邮箱"
            return render(request, "email.html", {"t_tip": t_tip})
    return render(request, "email.html")






def dianqi(request):
    thing_list = models.upthing.objects.filter(type='电器')
    print(thing_list)
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(thing_list, 8)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            things = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            things = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            things = paginator.page(paginator.num_pages)

    template_view = 'sort.html'
    return render(request, template_view, {'things': things })


def shuben(request):
    thing_list = models.upthing.objects.filter(type='书本')
    print(thing_list)
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(thing_list, 8)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            things = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            things = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            things = paginator.page(paginator.num_pages)

    template_view = 'sort.html'
    return render(request, template_view, {'things': things })


def shenghuoyongpin(request):
    thing_list = models.upthing.objects.filter(type='生活用品')
    print(thing_list)
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(thing_list, 8)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            things = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            things = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            things = paginator.page(paginator.num_pages)

    template_view = 'sort.html'
    return render(request, template_view, {'things': things })


def jiaotong(request):
    thing_list = models.upthing.objects.filter(type='交通工具')
    print(thing_list)
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(thing_list, 8)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            things = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            things = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            things = paginator.page(paginator.num_pages)

    template_view = 'sort.html'
    return render(request, template_view, {'things': things })
def qita(request):
    thing_list = models.upthing.objects.filter(type='其他')
    print(thing_list)
    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(thing_list, 8)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            things = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            things = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            things = paginator.page(paginator.num_pages)

    template_view = 'sort.html'
    return render(request, template_view, {'things': things })


def search(request):
    if request.method == "POST":
        thing_name = request.POST.get('thing_name')
        print(thing_name)


        thing_list = models.upthing.objects.filter(type=thing_name)

        # 将数据按照规定每页显示 10 条, 进行分割
        paginator = Paginator(thing_list, 8)


        if request.method == "POST":
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                things = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                things = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                things = paginator.page(paginator.num_pages)

        template_view = 'thingStore.html'
        return render(request, template_view, {'things': things })

def qiugou(request):

    need_list = models.upneed.objects.order_by("data")

    return render(request, "need.html", {'need_list':need_list})

def upneed(request):
    username = request.session.get('username', '')
    if not username:
        return redirect("/login/")
    if request.method == "POST":
        form = upneedform(request.POST)
        if form.is_valid():
                name = request.POST.get('name')
                price = request.POST.get('price')
                link = request.POST.get('link')
                detail = request.POST.get('detail')
                new_need = models.upneed.objects.create()
                new_need.upName = username
                new_need.name = name
                new_need.price = price
                new_need.link = link
                new_need.dTail = detail
                new_need.save()
                seccse_date = '上传成功，'
                return render(request, 'upneed.html', {'seccse':seccse_date})
        else:
            print()
            error_date = '输入有误，'
            return render(request, 'upneed.html', {'error': error_date})
    return render(request, "upneed.html", )



