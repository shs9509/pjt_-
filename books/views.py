from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from .models import Book, Comment
from .forms import Book_Form, Comment_Form

# Create your views here.

def index(request):
    books = Book.objects.order_by('-pk')
    genres = Book.objects.all().order_by('-genre').values_list('genre', flat=True).distinct()
    context = {
        'books': books,
        'genres':genres,
    }
    return render(request, 'books/index.html', context)

def genre(request,book_genre):
    books = Book.objects.order_by('-pk')
    genres = Book.objects.all().order_by('-genre').values_list('genre', flat=True).distinct()
    context = {
        'books': books,
        'genres':genres,
        'book_genre':book_genre,
    }
    return render(request,'books/genre.html',context)

@login_required
def create(request):
    if request.method == 'POST':
        book = Book_Form(request.POST, request.FILES)
        if book.is_valid():
            book = book.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('books:detail', book.pk)
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
    avg_rank = book.comment_set.all().aggregate(Avg('rank'))
    context = {
        'book' : book,
        'comment_form' : comment_form,
        'comments' : comments,
        'avg_rank' : avg_rank,
    }
    return render(request, 'books/detail.html', context )


@login_required
def delete(request,pk):
    book = get_object_or_404(Book, pk= pk)
    book.delete()
    return redirect('books:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request,pk):
    book = get_object_or_404(Book, pk = pk)
    if request.user == book.user:
        if request.method == 'POST':
            form = Book_Form(request.POST,request.FILES, instance = book)
            if form.is_valid():
                form.save()
                return redirect('books:detail', book.pk)
        else:
            form = Book_Form(instance=book)
    else:
        return redirect('books:index')
    context={
        'form' : form,
        'book' : book,
    }
    return render(request, 'books/update.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=pk)
        comment_form = Comment_Form(request.POST)
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
def likes(request,book_pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=book_pk)
        if request.user in book.like_user.all():
            book.like_user.remove(request.user)
        else:
            book.like_user.add(request.user)
        return redirect('books:index')
    return redirect('accounts:login')
