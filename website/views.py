from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, UpdateView, DeleteView


# forms --------------------------------------------------------------------------

class SignUpForm(UserCreationForm):
    Email = forms.EmailField(max_length=250, help_text='please type a valid email address')

    class Meta:
        model = User
        fields = ('username', 'Email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": "نام کاربری"})
        self.fields['Email'].widget.attrs.update({"placeholder": "ایمیل"})
        self.fields['password1'].widget.attrs.update({"placeholder": "رمز عبور"})
        self.fields['password2'].widget.attrs.update({"placeholder": "تکرار رمز عبور"})

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": "نام کاربری"})
        self.fields['password'].widget.attrs.update({"placeholder": "رمز عبور"})

class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('comment_body', 'date')
    
    widgets = {
        'comment_body':forms.Textarea(),
        'date':forms.DateField(),
    }

CHOICES = (
    ('1', 'براساس تاریخ--نزولی'),
    ('2', 'براساس تاریخ--صعودی'),
    ('3', 'براساس بازدید--نزولی'),
    ('4', 'براساس بازدید--صعودی'),
)


class FilterForm(forms.Form):
    field = forms.ChoiceField(choices=CHOICES)


# Create your views here -------------------------------------------------------------------

def SearchList(request):
    searched = request.GET.get('searched')
    if searched != "" and searched is not None:
        mark_articles = post.objects.filter(title__contains=searched) | post.objects.filter(
            post_body__contains=searched)
        paginator = Paginator(mark_articles, 3)
        page_number = request.GET.get('page')
        articles = paginator.get_page(page_number)
    else:
        articles = None

    context = {
        "searched": searched,
        "articles": articles
    }
    return render(request, 'website/search_list.html', context)


def main(request):
    promoted_article = post.objects.filter(promoted=True)[0]
    new_articles = post.objects.all().order_by('-date')[0:2]
    articles_list = post.objects.all().order_by('-date')[2:]
    best_article = post.objects.order_by('-views_number')[0]
    paginator = Paginator(articles_list, 3)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    context = {
        "articles": articles,
        "promoted_article": promoted_article,
        "new_articles": new_articles,
        "best_article": best_article
    }

    return render(request, 'website/mainPage.html', context)


def related(request, id):
    article = get_object_or_404(post, id=id)
    new_articles = post.objects.all().order_by('-date')[:4]
    article.views_number += 1
    article.save()
    context = {
        "article": article,
        "new_articles": new_articles
    }
    return render(request, 'website/relate.html', context)


def listt(request):
    form = FilterForm(initial={'field': '1'})
    articles_list = post.objects.all().order_by('-date')

    temp = request.GET.get('field')
    if temp == '1':
        articles_list = post.objects.all().order_by('-date')
        form = FilterForm(initial={'field': '1'})
    elif temp == '2':
        articles_list = post.objects.all().order_by('date')
        form = FilterForm(initial={'field': '2'})

    elif temp == '3':
        articles_list = post.objects.all().order_by('-views_number')
        form = FilterForm(initial={'field': '3'})

    elif temp == '4':
        articles_list = post.objects.all().order_by('views_number')
        form = FilterForm(initial={'field': '4'})

    min_date = request.GET.get('min')
    max_date = request.GET.get('max')
    if min_date and max_date:
        articles_list = articles_list.filter(date__range=[min_date, max_date])

    paginator = Paginator(articles_list, 3)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    best_articles = post.objects.all().order_by('-views_number')
    paginator2 = Paginator(best_articles, 2)
    page_number2 = request.GET.get('page2')
    best_articles = paginator2.get_page(page_number2)

    more_comments = post.objects.annotate(comments_number=models.Count('comments', filter=models.Q(comments__accepted=True))).order_by('-comments_number')
    paginator3 = Paginator(more_comments, 2)
    page_number3 = request.GET.get('page3')
    more_comments = paginator3.get_page(page_number3)

    context = {
        "articles": articles,
        "form": form,
        "best_articles": best_articles,
        "more_comments": more_comments,
        "temp": temp,
        "max": max_date,
        "min": min_date
    }
    return render(request, 'website/listpage.html', context)

def userpanel(request):
    allposts = post.objects.all().order_by('-date')
    paginator = Paginator(allposts, 3)
    page_number = request.GET.get('page')
    allposts = paginator.get_page(page_number)
    return render(request, 'website/userpanel.html', context={'allposts': allposts})


# Narjes's part ------------------------------------------------------------------

def signUp(request):
    if request.method == "POST":
        filledform = SignUpForm(request.POST)
        if filledform.is_valid():
            filledform.save()
            username = filledform.cleaned_data.get('username')
            passw = filledform.cleaned_data.get('password1')
            new_user = authenticate(username=username, password=passw)
            login(request, new_user)
            return redirect('userpanel')
    else:
        filledform = SignUpForm()
    return render(request, 'website/signup.html', context={'form': filledform})


def logIn(request):
    if request.method == "POST":
        filledform = SignInForm(data=request.POST)
        if filledform.is_valid():
            user = filledform.get_user()
            login(request, user)
            return redirect('userpanel')
    else:
        filledform = SignInForm()
    return render(request, 'website/logIn.html', context={'form': filledform})


class AddPost(CreateView):
    model = post
    template_name = "newpost.html"
    fields = ['title', 'post_body', 'image', 'date', 'views_number']

    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.author = self.request.user
        form.save()

        return super().form_valid(form)


class EditPost(UpdateView):
    model = post
    template_name = "Editpost.html"
    fields = ['title', 'post_body', 'image', 'date', 'views_number']


class Deletepost(DeleteView):
    model = post
    template_name = "Deletepost.html"


class Addcomment(CreateView):
    model = comment
    template_name = "addcomment.html"
    form_class = commentForm

    def form_valid(self, form):
        postt = get_object_or_404(post, id= self.kwargs['pk'])
        if postt.author == self.request.user:
            form.instance.accepted = True
        form.instance.author = self.request.user.get_username()
        form.instance.post = postt
        form.save()

        return super().form_valid(form)


class replycomment(CreateView):
    model = comment
    template_name = "addcomment.html"
    form_class = commentForm

    def form_valid(self, form):
        postt = get_object_or_404(post, id= self.kwargs['pk'])
        replied =get_object_or_404(comment, id= self.kwargs['pk_alt'])
        if postt.author == self.request.user:
            form.instance.accepted = True
        form.instance.author = self.request.user.get_username()
        form.instance.post = postt
        form.instance.root = replied
        form.save()

        return super().form_valid(form)


def submit_comment(request, id):
    commentt =get_object_or_404(comment, id=id)
    if request.method == 'POST':
        commentt.accepted = True
        commentt.save()
    return redirect('userpanel')