from django.contrib.gis.forms import OSMWidget


class CustomMapWidget(OSMWidget):
    template_name = "openlayers-osm.html"
