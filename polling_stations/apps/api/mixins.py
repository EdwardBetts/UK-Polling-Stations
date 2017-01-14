from rest_framework.decorators import list_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000


class PollingEntityMixin():

    pagination_class = LargeResultsSetPagination

    def output(self, request):
        if not self.validate_request():
            return Response(
                {'detail': 'council_id parameter must be specified'}, 400)

        queryset = self.get_queryset()

        if 'council_id' not in request.query_params:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(
                    page,
                    many=True,
                    read_only=True,
                    context={'request': request}
                )
                return self.get_paginated_response(serializer.data)

        if 'council_id' in request.query_params and (
                'station_id' in request.query_params or
                'district_id' in request.query_params) and\
                len(queryset) == 1:
            # If we are requesting a single polling station or district
            # return an object instead of an array with length 1
            serializer = self.get_serializer(
                queryset[0],
                many=False,
                read_only=True,
                context={'request': request}
            )
            return Response(serializer.data)

        serializer = self.get_serializer(
            queryset,
            many=True,
            read_only=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        self.geo = False
        return self.output(request)

    @list_route(url_path='geo')
    def geo(self, request, format=None):
        self.geo = True
        return self.output(request)
