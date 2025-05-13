from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.conf import settings
from rest_framework import status
from django.db.models import F
import math
from .models import Gym, Court, Team, Player, Manager
from .serializers import GymSerializer, CourtSerializer, TeamSerializer, PlayerSerializer, ManagerSerializer

class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        zip_code = request.query_params.get('zip')

        if zip_code and (not lat or not lon):
            # Use OpenStreetMap Nominatim to get coordinates from zip
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
            R = 6371
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c

        gyms = Gym.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
        gyms_with_distance = [(gym, haversine(lat, lon, gym.latitude, gym.longitude)) for gym in gyms]
        gyms_with_distance.sort(key=lambda x: x[1])

        serializer = self.get_serializer([g[0] for g in gyms_with_distance], many=True)
        return Response(serializer.data)

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
