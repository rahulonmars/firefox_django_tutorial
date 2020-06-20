from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from catalog.models import Book, BookInstance, Author, Genre
from catalog.forms import RenewBookModelForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back':proposed_renewal_date})
    
    context ={
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html',context)

def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()

    #Available Books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    genres_romance = Genre.objects.filter(name__icontains='romance').count()
    num_books_with_t = Book.objects.filter(title__icontains='t').count()

    #Number of visitors
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genre_romance':genres_romance,
        'num_books_with_t':num_books_with_t,
        'num_visits':num_visits,
    }

    # print(genres_romance)

    #Render the HTML template 
    return render(request, 'index.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin ,generic.ListView):
    """Books loaned to a User"""
    model= BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by=2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LibrarianBookBorrowDetails(PermissionRequiredMixin, generic.ListView):
    """All Books loaned by Users"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_librarian.html'

    permission_required = 'catalog.can_mark_returned'        

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    paginate_by = 2
    # queryset = Book.obects.filter(title__icontains='T')[:5]
    # template_name = ''

class BookDetailView(generic.DetailView):
    model = Book
    # context_object_name = 'my_book_detail'

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'my_author_list'
    paginate_by = 2
    # queryset = Book.obects.filter(title__icontains='T')[:5]
    # template_name = ''

class AuthorDetailView(generic.DetailView):
    model = Author
    # context_object_name = 'my_book_detail'

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death':'05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    # initial = {'date_of_death':'05/01/2018'}

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
