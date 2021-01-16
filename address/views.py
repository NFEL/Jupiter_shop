import sys
import folium
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.geos import Point
from django.http import HttpResponseBadRequest

from geopy import distance as dis
from ip2geotools.databases.noncommercial import DbIpCity

import urllib.request

from address import geolocator
from store.models import Store
from .models import StoreAddress, UserAddress
from .forms import UserLocationMarker


class ListAddressesMixIn():
    queryset = None

    def get_queryset(self):
        self.queryset = UserAddress.objects.filter(user=self.request.user)
        return self.queryset

    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)

        locations = []
        store_locations = set()

        for item in request.cart_items:
            store_locations.add(item.product.store)
        form = UserLocationMarker(request.POST or None)

        user_location = None
        if request.method == 'POST':
            form = UserLocationMarker(request.POST)

            if form.is_valid():
                user_location = self.point_parser(
                    request.POST.get('location' or None))
        
        # if request.method == 'POST':
        #     folium.vector_layers.Marker(user_location, icon=folium.Icon(
        #         color='green', prefix='glyphicon', icon='home')).add_to(map)

        store_locs= []
        for store in store_locations:
            for loc in StoreAddress.objects.filter(store = store):
                print(loc)
                sys.stdout.flush()
                location_corrected = (loc.location.y, loc.location.x)
                store_locs.append(location_corrected)
                # folium.vector_layers.Circle(
                #     location_corrected,
                #     float(loc.working_raduis),
                #     fill=True).add_to(map)

                # folium.vector_layers.Marker(location_corrected).add_to(map)

                # if request.method == 'POST':
                #     distance = dis.distance(
                #         user_location, Point(location_corrected)).km

                #     if distance > loc.working_raduis:
                #         folium.vector_layers.PolyLine(
                #             [user_location, location_corrected], popup='No service', tooltip="No service", color="#FF0000").add_to(map)
                #     else:
                #         distance_str = f'distance is {distance} km'
                #         folium.vector_layers.PolyLine(
                #             [user_location, location_corrected], popup=distance_str, tooltip=distance_str, color="#808000").add_to(map)

        # context['map'] = map._repr_html_() 
        context['form']= form
        context['stores'] = store_locs
        return context

        



    def point_parser(self, location):
        if isinstance(location, str):
            if location.__contains__('Point'):
                long = float(location.split('"coordinates":')
                             [1].split(',')[0][1:])
                lat = float(location.split('"coordinates":')
                            [1].split(',')[1][:-2])
                return Point((lat, long))
