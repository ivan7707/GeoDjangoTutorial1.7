from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.contrib.gis.gdal import DataSource
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
# Import system modules
import itertools
import tempfile
import os
# Import custom modules
from waypoints.models import Waypoint
import json



def index(request):
    waypoints = Waypoint.objects.order_by('name')
    template = loader.get_template('waypoints/index.html')
    context = RequestContext(request, {
        'waypoints': waypoints, 'content': render_to_string('waypoints/waypoints.html', {'waypoints': waypoints})
    })
    return HttpResponse(template.render(context))

@csrf_exempt
################## doesnt work without the @csrf_exempt.  Have to figure out why this is the case#########
def save(request):
    c = {}
    c.update(csrf(request))
    for waypointString in request.POST.get('waypointsPayload', '').splitlines():
        waypointID, waypointX, waypointY = waypointString.split()
        waypoint = Waypoint.objects.get(id=int(waypointID))
        waypoint.geometry.set_x(float(waypointX))
        waypoint.geometry.set_y(float(waypointY))
        waypoint.save()
    return HttpResponse(json.dumps(dict(isOk=1)), c)


def search(request):
    # Build searchPoint
    try:
        searchPoint = Point(float(request.GET.get('lng')), float(request.GET.get('lat')))
    except:
        return HttpResponse(json.dumps(dict(isOk=0, message='Could not parse search point')))
    # Search database
    waypoints = Waypoint.objects.distance(searchPoint).order_by('distance')
    # Return
    return HttpResponse(json.dumps(dict(
        isOk=1,
        content=render_to_string('waypoints/waypoints.html', {
            'waypoints': waypoints
        }),
        waypointByID=dict((x.id, {
            'name': x.name,
            'lat': x.geometry.y,
            'lng': x.geometry.x,
        }) for x in waypoints),
    )))


def upload(request):
    if 'gpx' in request.FILES:
        # Get
        try:
            gpxFile = request.FILES['gpx']
        except IOError:
            print("gpx")


        handle, targetPath = tempfile.mkstemp()
        destination = os.fdopen(handle, 'wb')
        for chunk in gpxFile.chunks():
            destination.write(chunk)
        destination.close()

        # Parse
        dataSource = DataSource(targetPath)

        layer = dataSource[0]
        waypointNames = layer.get_fields('name')
        waypointGeometries = layer.get_geoms()

        # name change from Python 2 to 3
        try:
            zip_longest = itertools.zip_longest  # Python 3
        except AttributeError:
            zip_longest = itertools.izip_longest  # Python 3

        for waypointName, waypointGeometry in zip_longest(waypointNames, waypointGeometries):
            waypoint = Waypoint(name=waypointName, geometry=waypointGeometry.wkt)
            waypoint.save()

        # Clean up: took out the os.remove(targetPath)


    return HttpResponseRedirect(reverse('waypoints-index'))
