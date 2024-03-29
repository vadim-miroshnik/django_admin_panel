from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from movies.models import Filmwork, PersonFilmWork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def _aggregate_person(self, role):
        return ArrayAgg('persons__full_name', filter=Q(personfilmwork__role=role), distinct=True)

    def get_queryset(self):
        fw = Filmwork.objects.filter().values('id', 'title', 'description', 'creation_date', 'rating', 'type').annotate(
            genres=ArrayAgg('genres__name', distinct=True), 
            actors=self._aggregate_person(role=PersonFilmWork.Role.actor),
            directors=self._aggregate_person(role=PersonFilmWork.Role.director),
            writers=self._aggregate_person(role=PersonFilmWork.Role.writer))
        return fw

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        prev_page = page.previous_page_number() if page.has_previous() else None
        next_page = page.next_page_number() if page.has_next() else None
        return {'count': paginator.count,
                'total_pages': paginator.num_pages,
                'prev': prev_page,
                'next': next_page,
                'results': list(page)
                }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context['object']

