from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Comment
from .forms import Book_Form, Comment_Form

# Create your views here.

def index(request):
    books = Book.objects.order_by('-pk')
    context = {
        'books': books,
    }
    return render(request, 'books/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        book = Book_Form(request.POST, request.FILES)
        if book.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = Book_Form()
    context = {
        'form': form, 
    }
    return render(request,'books/create.html',context)


def detail(request,pk):
    book = get_object_or_404(Book, pk=pk)
    comment_form = Comment_Form()
    comments = book.comment_set.all()
    context = {
        'book' : book,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, 'books/detail.html', context )


@login_required
def delete(request,pk):
    book = get_object_or_404(Book, pk= pk)
    book.delete()
    return redirect('books:index')


@login_required
def update(request,pk):
    book = get_object_or_404(Book, pk = pk)
    if request.method == 'POST':
        form = Book_Form(request.POST, instance = book)
        if form.is_valid():
            form.save()
            return redirect('books:detail', pk)
    else:
        form = Book_Form(instance=book)
    context={
        'form' : form,
        'book' : book,
    }
    return render(request, 'books/update.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
            return redirect('books:detail', book.pk)
        context = {
            'comment_form': comment_form,
            'book': book,
        }
        return render(request, 'books/detail.html', context)
    return redirect('accounts:login')


@require_POST
def likes(request,pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=pk)
        if request.user in book.like_users.all():
            book.like_users.remove(request.user)
        else:
            book.like_users.add(request.user)
        return redirect('books:index')
    return redirect('accounts:login')
