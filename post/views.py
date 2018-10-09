try:
    from urllib.parse import quote_plus #python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from comment.forms import CommentForm
from comment.models import Comment
from .models import Post

# Create your views here.

def post_list(request):
    all_post = Post.objects.all()
    context = {
        'all_post': all_post,
    }
    template = 'post/list.html'
    return render(request, template, context)


def post_detail(request, id=None):
    instance = Post.objects.get(id=id)
    share_string = quote_plus(instance.content)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        print('working')
        comment = form.save(commit=False)
        c_type = comment.content_type
        comment.content_type = ContentType.objects.get(model=c_type)
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        comment.parent = parent_obj
        new_comment = comment.save()
        return redirect('detail', id=instance.id)

    comments = instance.comments
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
        'comments': comments,
        'comment_form': form,
    }
    template = 'post/detail.html'
    return render(request, template, context)
