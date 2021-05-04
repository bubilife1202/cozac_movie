from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, FreePostForm, FreeCommentForm
from .models import Post, FreePost
from django.core.paginator import Paginator

def home(request):
    # posts = Post.objects.all()
    posts = Post.objects.filter().order_by('-date')
    paginator = Paginator(posts, 5)
    pagnum = request.GET.get('page')
    posts = paginator.get_page(pagnum)

    return render(request, 'index.html', {'posts':posts})

def postcreate(request):
    # request method가 POST일 경우
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form':form})

def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm()
    return render(request, 'detail.html', {'post_detail':post_detail, 'comment_form': comment_form})

# 게시물 삭제
def delete(request, post_id):
    delete_post = get_object_or_404(Post, pk=post_id)
    delete_post.delete()
    return redirect('home')

# 게시물 수정
def edit(request, post_id):
    post = Post.objects.get(id=post_id)    # 수정하고자 하는 객체 갖고 와서
    if request.method == "POST":            # 만일 request method가 POST라면
        form = PostForm(request.POST, request.FILES)    # 입력 내용을 갖고와서
        if form.is_valid():                             # 입력 내용 검수한 뒤
            post.title = form.cleaned_data['title']     # 입력 내용 중 title을 수정하고자 하는 객체의 title에 저장!
            post.body = form.cleaned_data['body']       # 입력 내용 중 body를 수정하고자 하는 객체의 body에 저장!
            post.save()                                 # 그리고 수정된 값을 저장한 객체는 저장
            return redirect('/detail/'+str(post.pk))      # 수정이 되었으면 detail 페이지(해당 그 게시물 페이지)로 이동
    else:                                        # 만일 request method가 GET이면
        form = PostForm()                  
        return render(request, 'form_edit.html',{'form':form})  # 입력 공간을 갖다준다

# 댓글 저장
def new_comment(request, post_id):
    filled_form = CommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Post, pk=post_id)
        finished_form.save()
    return redirect('detail', post_id)

def freehome(request):
    # posts = Post.objects.all()
    freeposts = FreePost.objects.filter().order_by('-date')
    return render(request, 'free_index.html', {'freeposts':freeposts})

def freepostcreate(request):
    # request method가 POST일 경우
    if request.method == 'POST' or request.method == 'FILES':
        form = FreePostForm(request.POST, request.FILES)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.author = request.user
            unfinished.save()
            return redirect('freehome')
    else:
        form = FreePostForm()
    return render(request, 'free_post_form.html', {'form':form})

def freedetail(request, post_id):
    post_detail = get_object_or_404(FreePost, pk=post_id)
    comment_form = FreeCommentForm()
    return render(request, 'free_detail.html', {'post_detail':post_detail, 'comment_form': comment_form})

# 게시물 삭제
def freedelete(request, post_id):
    delete_post = get_object_or_404(FreePost, pk=post_id)
    delete_post.delete()
    return redirect('freehome')

# 게시물 수정
def freeedit(request, post_id):
    post = FreePost.objects.get(id=post_id)    # 수정하고자 하는 객체 갖고 와서
    if request.method == "POST":            # 만일 request method가 POST라면
        form = FreePostForm(request.POST, request.FILES)    # 입력 내용을 갖고와서
        if form.is_valid():                             # 입력 내용 검수한 뒤
            post.title = form.cleaned_data['title']     # 입력 내용 중 title을 수정하고자 하는 객체의 title에 저장!
            post.body = form.cleaned_data['body']       # 입력 내용 중 body를 수정하고자 하는 객체의 body에 저장!
            post.save()                                 # 그리고 수정된 값을 저장한 객체는 저장
            return redirect('/freedetail/'+str(post.pk))      # 수정이 되었으면 detail 페이지(해당 그 게시물 페이지)로 이동
    else:                                        # 만일 request method가 GET이면
        form = FreePostForm()                  
        return render(request, 'free_form_edit.html',{'form':form})  # 입력 공간을 갖다준다

# 댓글 저장
def new_freecomment(request, post_id): 
    filled_form = FreeCommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(FreePost, pk=post_id)
        finished_form.save()
    return redirect('freedetail', post_id)