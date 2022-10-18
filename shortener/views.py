from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from shortener.models import Link, Location
from shortener.serializers import LinkSerializer, PublicLinkSerializer
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Count

class LinkViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkSerializer

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user).order_by('-created_at')
    

class NewView(APIView):
    def post(self, request):
        link = get_object_or_404(Link, url_code=request.data['url_code'])
        serializer = PublicLinkSerializer(link)

        # get user ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # get user location
        geo = GeoIP2()
        country = geo.country(ip)
        print(country)
        print(ip)

        if request.data.get("has_seen", 0) == 1:
            return Response({
                'status': 'success',
                'data': {
                    'url': serializer.data
                }
            })
        elif request.data.get("has_seen", 0) == 0:
            location = Location.objects.filter(link=link, ip=ip).first()
            if location:
                return Response({
                    'status': 'success',
                    'data': {
                        'url': serializer.data
                    }
                })
            else:
                link.view += 1
                link.save()
                Location.objects.create(user=link.user, link=link, ip=ip, country=country['country_name'], country_code=country['country_code'])
                return Response({
                    'status': 'success',
                    'data': {
                        'url': serializer.data
                    }
                })

class LocationsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, url_code):
        link = Link.objects.get(user=request.user, url_code=url_code)
        locations = Location.objects.filter(link=link).values("country").distinct().count()
        return Response({
            'status': 'success',
            'data': locations
        })


class AllLocationsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        locations = Location.objects.filter(user=request.user).values("country", "country_code").annotate(Count("id")).order_by('-id__count')

        return Response({
            'status': 'success',
            'data': locations
        })


class NumberOfViewsAndLinksView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        number = Link.objects.filter(user=request.user).count()
        links = Link.objects.filter(user=request.user).all()

        views = 0
        for link in links:
            views = views + link.view

        print(views)
        print(number)
        return Response({
            'status': 'success',
            'data': {
                "number": number,
                "views": views
            }
        })

