from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment


def comment_thread(request, id):
    #obj = Comment.objects.get(id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent

    content_object = obj.content_object # Post that the comment is on
    content_id = obj.content_object.id

    initial_data = {
            "content_type": obj.content_type,
            "object_id": obj.object_id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
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
        comment.save()
        return HttpResponseRedirect(comment.content_object.get_absolute_url())


    context = {
        "comment": obj,
        "form": form,
    }
    return render(request, "post/thread.html", context)
