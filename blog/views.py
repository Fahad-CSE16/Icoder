from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

def blogHome(request):
    myposts=Post.objects.all()
    # print(myposts)
    return render(request, 'blog/blogHome.html',{'myposts':myposts})
    #return HttpResponse('bloghome')
    #FOR SHOWING AFTER ACCESS DATABASE
    #myposts= Blogpost.objects.all()
    #return render(request, 'blog/index.html',{'myposts':myposts})

# def blogPost(request, mid):
#     post = Post.objects.filter(sno=mid)[0]
#     return render(request, 'blog/blogPost.html',{'post':post})

def blogPost(request, slug):
    post= Post.objects.filter(slug=slug).first()
    post.views= post.views + 1
    post.save()
    comments=BlogComment.objects.filter(post=post, parent= None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
        
    return render(request, 'blog/blogPost.html',{'post': post, 'comments':comments,'replyDict': replyDict})

def postComment(request):
    if request.method=="POST":
        comment= request.POST.get("comment")
        user = request.user 
        postsno=request.POST.get("postsno")
        post =  Post.objects.get(sno=postsno) 
        parentsno =  request.POST.get("parentsno") 
        if parentsno == "":
            comments= BlogComment(comment=comment, user= user, post= post)
            comments.save()
            messages.success(request, 'Success! your comment have been posted successfully.')
        else:
            parent=BlogComment.objects.get(sno=parentsno)
            comments= BlogComment(comment=comment, user= user, post= post, parent=parent)
            comments.save()
            messages.success(request, 'Success! your reply have been posted successfully.')
    return redirect(f"/blog/{post.slug}")