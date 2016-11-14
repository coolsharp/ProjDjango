from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.http import HttpResponse
import requests


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'coolsharp/api/main.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# 크로스 도메인 문제를 해결하기 위해 API에서 호출
def getApi(request):
    url = request.GET.get('url', '')
    r = requests.get(url, stream=True)

    return HttpResponse(r.text)
