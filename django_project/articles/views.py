from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse

from .forms import CommentForm
from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    """
    ArticleListView displays a list of articles.

    @param: LoginRequiredMixin (Django mixin), ListView (Django generic view)
    @desc: This view requires user authentication and extends Django's ListView. It lists articles using the Article model and renders them in the "article_list.html" template.
    @returns: Rendered HTML page with a list of articles.
    """

    model = Article
    template_name = "article_list.html"


class CommentGet(DetailView):
    """
    CommentGet handles the display of article details with a comment form.

    @param: DetailView (Django generic view)
    @desc: This view extends Django's DetailView, associated with the Article model. It displays article details in the "article_detail.html" template and includes a comment form.
    @returns: Rendered HTML page with article details and a comment form.
    """

    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        """
        get_context_data() is used to pass additional context to the template.

        @param: self (Django view), **kwargs (Django view)
        @desc: This method is used to pass additional context to the template. It includes a comment form.
        @returns: Rendered HTML page with article details and a comment form.
        """
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    """
    CommentPost handles the submission of comments on an article.

    @param: SingleObjectMixin (Django mixin), FormView (Django generic view)
    @desc: This view extends Django's FormView and is associated with the Article model. It allows users to submit comments on an article in the "article_detail.html" template.
    @returns: Form submission handling for article comments.
    """

    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        """
        post() handles POST requests.

        @param: self (Django view), request (Django view), *args (Django view), **kwargs (Django view)
        @desc: This method handles POST requests. It uses the get_object() method to retrieve the article object and the form_valid() method to validate the form.
        @returns: Form submission handling for article comments.
        """
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        form_valid() validates the form.

        @param: self (Django view), form (Django view)
        @desc: This method validates the form. It uses the get_object() method to retrieve the article object and the form_valid() method to validate the form.
        @returns: Form submission handling for article comments.
        """
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        get_success_url() redirects to the article detail page.

        @param: self (Django view)
        @desc: This method redirects to the article detail page.
        @returns: Form submission handling for article comments.
        """

        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    """
    ArticleDetailView handles article detail views.

    @param: LoginRequiredMixin (Django mixin), View (Django generic view)
    @desc: This view provides the ability to view article details. It uses CommentGet.as_view() for GET requests and CommentPost.as_view() for POST requests.
    @returns: Rendered HTML page with article details and comment submission.
    """

    def get(self, request, *args, **kwargs):
        """
        get() handles GET requests.

        @param: self (Django view), request (Django view), *args (Django view), **kwargs (Django view)
        @desc: This method handles GET requests. It uses CommentGet.as_view() for GET requests and CommentPost.as_view() for POST requests.
        @returns: Rendered HTML page with article details and comment submission.
        """

        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        post() handles POST requests.

        @param: self (Django view), request (Django view), *args (Django view), **kwargs (Django view)
        @desc: This method handles POST requests. It uses CommentGet.as_view() for GET requests and CommentPost.as_view() for POST requests.
        @returns: Rendered HTML page with article details and comment submission.
        """

        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    ArticleUpdateView allows users to edit and update articles.

    @param: LoginRequiredMixin (Django mixin), UserPassesTestMixin (Django mixin), UpdateView (Django generic view)
    @desc: This view requires user authentication and checks if the user is the author of the article using UserPassesTestMixin. Users can edit and update article titles and bodies using the "article_edit.html" template.
    @returns: Rendered HTML page with a form to edit and update articles.
    """

    model = Article
    fields = ("title", "body")
    template_name = "article_edit.html"

    def test_func(self):
        """
        test_func() checks if the user is the author of the article.

        @param: self (Django view)
        @desc: This method checks if the user is the author of the article.
        @returns: Rendered HTML page with a form to edit and update articles.
        """

        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    ArticleDeleteView allows users to delete articles.

    @param: LoginRequiredMixin (Django mixin), UserPassesTestMixin (Django mixin), DeleteView (Django generic view)
    @desc: This view requires user authentication and checks if the user is the author of the article using UserPassesTestMixin. Users can delete articles, and upon successful deletion, they are redirected to the article list page.
    @returns: Deletion of articles and redirection to the article list.
    """

    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        """
        test_func() checks if the user is the author of the article.

        @param: self (Django view)
        @desc: This method checks if the user is the author of the article.
        @returns: Deletion of articles and redirection to the article list.
        """

        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    ArticleCreateView allows users to create new articles.

    @param: LoginRequiredMixin (Django mixin), CreateView (Django generic view)
    @desc: This view requires user authentication and allows users to create new articles with titles and bodies. The "article_new.html" template is used for article creation.
    @returns: Rendered HTML page with a form to create new articles.
    """

    model = Article
    template_name = "article_new.html"
    fields = ("title", "body")

    def form_valid(self, form):
        """
        form_valid() validates the form.

        @param: self (Django view), form (Django view)
        @desc: This method validates the form. It uses the get_object() method to retrieve the article object and the form_valid() method to validate the form.
        @returns: Form submission handling for article comments.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)
