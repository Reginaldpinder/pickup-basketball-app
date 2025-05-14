from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.conf import settings
from rest_framework import status
from django.db.models import F
import math
from .models import Gym , Court, Team, Player, Manager
from .serializers import GymSerializer , CourtSerializer, TeamSerializer, PlayerSerializer, ManagerSerializer

class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        zip_code = request.query_params.get('zip')
        radius_km = float(request.query_params.get('radius', 25))  # default 25 km (~15 miles)

        if zip_code and (not lat or not lon):
            # Use OpenStreetMap to resolve zip code
            resp = requests.get(f'https://nominatim.openstreetmap.org/search',
                                params={'postalcode': zip_code, 'format': 'json', 'countrycodes': 'us'})
            if resp.status_code == 200 and resp.json():
                location = resp.json()[0]
                lat = float(location['lat'])
                lon = float(location['lon'])
            else:
                return Response({'error': 'Invalid zip code'}, status=400)

        if lat is None or lon is None:
            return Response({'error': 'Missing coordinates or zip code'}, status=400)

        lat = float(lat)
        lon = float(lon)

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth radius in km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c

        gyms = Gym.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
        gyms_with_distance = [
            (gym, haversine(lat, lon, gym.latitude, gym.longitude))
            for gym in gyms
        ]

        gyms_in_radius = [g[0] for g in gyms_with_distance if g[1] <= radius_km]
        gyms_in_radius.sort(key=lambda g: haversine(lat, lon, g.latitude, g.longitude))  # sort by closest

        serializer = self.get_serializer(gyms_in_radius, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def external(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        radius_m = int(request.query_params.get('radius', 5000))

        if not lat or not lon:
            return Response({'error': 'Missing lat/lon'}, status=400)

        query = f"""
        [out:json];
        (
        node["leisure"="pitch"]["sport"="basketball"](around:{radius_m},{lat},{lon});
        way["leisure"="pitch"]["sport"="basketball"](around:{radius_m},{lat},{lon});
        relation["leisure"="pitch"]["sport"="basketball"](around:{radius_m},{lat},{lon});
        );
        out center;
        """

        try:
            response = requests.get("https://overpass-api.de/api/interpreter", params={'data': query})
            data = response.json()

            gyms = []
            for el in data.get('elements', []):
                tags = el.get('tags', {})
                name = tags.get('name', 'Unnamed Court')

                # Use lat/lon directly for nodes
                if el['type'] == 'node':
                    lat_val = el['lat']
                    lon_val = el['lon']
                # Use center for way/relation
                elif el['type'] in ['way', 'relation'] and 'center' in el:
                    lat_val = el['center']['lat']
                    lon_val = el['center']['lon']
                else:
                    continue

                gyms.append({
                    'name': name,
                    'latitude': lat_val,
                    'longitude': lon_val,
                    'location': tags.get('addr:full') or tags.get('addr:street') or 'Unknown'
                })

            return Response(gyms)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class CourtViewSet(viewsets.ModelViewSet):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer