# Standard Python Library imports.
from functools import reduce
import operator

# Core Django imports.
from django.contrib import messages
from django.db.models import Q
from django.views.generic import (
    DetailView,
    ListView,
)

# Blog application imports.
from blog.models.showcase_models import Showcase
from blog.models.category_models import Category
from blog.forms.blog.comment_forms import CommentForm


class ShowcaseListView(ListView):
    context_object_name = "showcases"
    paginate_by = 12
    queryset = Showcase.objects.filter(status=Showcase.PUBLISHED, deleted=False)
    template_name = "blog/showcase/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class ShowcaseDetailView(DetailView):
    model = Showcase
    template_name = 'blog/showcase/showcase_detail.html'

    def get_context_data(self, **kwargs):
        session_key = f"viewed_showcase {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True

        kwargs['related_showcase'] = \
            Showcase.objects.filter(category=self.object.category, status=Showcase.PUBLISHED).order_by('?')[:3]
        kwargs['showcase'] = self.object
        kwargs['comment_form'] = CommentForm()
        return super().get_context_data(**kwargs)


class ShowcaseSearchListView(ListView):
    model = Showcase
    paginate_by = 12
    context_object_name = 'search_results'
    template_name = "blog/showcase/showcase_search_list.html"

    def get_queryset(self):
        """
        Search for a user input in the search bar.

        It pass in the query value to the search view using the 'q' parameter.
        Then in the view, It searches the 'title', 'slug', 'body' and fields.

        To make the search a little smarter, say someone searches for
        'container docker ansible' and It want to search the records where all
        3 words appear in the showcase content in any order, It split the query
        into separate words and chain them.
        """

        query = self.request.GET.get('q')

        if query:
            query_list = query.split()
            search_results = Showcase.objects.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(slug__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(body__icontains=q) for q in query_list))
            )

            if not search_results:
                messages.info(self.request, f"No results for '{query}'")
                return search_results.filter(status=Showcase.PUBLISHED, deleted=False)
            else:
                messages.success(self.request, f"Results for '{query}'")
                return search_results.filter(status=Showcase.PUBLISHED, deleted=False)
        else:
            messages.error(self.request, f"Sorry you did not enter any keyword")
            return []

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ShowcaseSearchListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class TagShowcasesListView(ListView):
    """
        List showcasess related to a tag.
    """
    model = Showcase
    paginate_by = 12
    context_object_name = 'tag_showcases_list'
    template_name = 'blog/showcase/tag_showcases_list.html'

    def get_queryset(self):
        """
            Filter Showcases by tag_name
        """

        tag_name = self.kwargs.get('tag_name', '')

        if tag_name:
            tag_showcases_list = Showcase.objects.filter(tags__name__in=[tag_name],
                                                       status=Showcase.PUBLISHED,
                                                       deleted=False
                                                       )

            if not tag_showcases_list:
                messages.info(self.request, f"No Results for '{tag_name}' tag")
                return tag_showcases_list
            else:
                messages.success(self.request, f"Results for '{tag_name}' tag")
                return tag_showcases_list
        else:
            messages.error(self.request, "Invalid tag")
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context
