from urllib.parse import quote_plus
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
def post_list(request):
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    else:
        queryset_list = Post.objects.active()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(content__icontains=query)|Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query)).distinct()
    paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
    page_request_var = 'abc'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
        # If page is not an integer, deliver first page.
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    # return render(request, 'list.html', {'contacts': contacts})
    today = timezone.now().date()

    context = {
    "objList" : queryset,
    "page_request_var" : page_request_var,
    "today" : today,
    }
    return render(request,"posts_list.html",context)
    # return HttpResponse("<h1>PostList</h1>")

        # contact_list = Contacts.objects.all()



def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post_form = PostForm(request.POST or None,request.FILES or None)
    if post_form.is_valid():
        instance = post_form.save(commit = False)
        instance.save()
        messages.success(request,"Successfully Added")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "post_form" : post_form,
    }
    return render(request,"posts_create.html",context)
    # return HttpResponse("<h1>PostList</h1>")

def post_detail(request,slug = None):
    instance = get_object_or_404(Post,slug = slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    # queryset = Post.objects.all()
    context = {
        "instance" : instance,
        "share_string" : share_string,
    }
    return render(request,"posts_detail.html",context)
    # return HttpResponse("<h1>PostList</h1>")

def post_update(request,slug = None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug = slug,)
    post_form = PostForm(request.POST or None,request.FILES or None,instance=instance)
    if post_form.is_valid():
        instance = post_form.save(commit = False)
        instance.user = request.user
        instance.save()
        messages.success(request,"<a href='#'>Item</a> Edited",extra_tags='some-tag')
        return HttpResponseRedirect(instance.get_absolute_url())
    # queryset = Post.objects.all()
    context = {
        "instance" : instance,
        "post_form" : post_form
    }
    return render(request,"posts_create.html",context)
    # return HttpResponse("<h1>PostList</h1>")

def post_delete(request,slug = None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug = slug)
    instance.delete()
    messages.success(request,"Successfully deleted")
    return redirect("posts:list")
