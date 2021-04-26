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

def create(request):
    if request.method == 'POST':
        book = Book_Form(request.POST, request.FILES)
        if book.is_valid():
            book.save()
            return redirect('books:index')
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


def delete(request,pk):
    book = get_object_or_404(Book, pk= pk)
    book.delete()
    return redirect('books:index')

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


