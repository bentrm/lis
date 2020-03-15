from collections import OrderedDict

from django.contrib.gis.geos import Point, MultiPoint
from rest_framework import pagination
from rest_framework.response import Response


class MemorialPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        if len(data) >= 2:
            points = [Point(memorial['position']) for memorial in data]
            bbox = MultiPoint(points).envelope
        else:
            bbox = MultiPoint(
                Point(12.1898, 49.9664),
                Point(15.5079, 49.9664),
                Point(15.5079, 51.4444),
                Point(12.1898, 51.4444),
            ).envelope
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('bbox', (bbox.coords[0][0], bbox.coords[0][2])),
        ]))
