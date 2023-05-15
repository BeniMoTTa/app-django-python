from django.shortcuts import render
from .models import Movie
from rest_framework.views import APIView, Response
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsAllowed
from rest_framework.pagination import PageNumberPagination


class MovieRegisterView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowed]
    
    def post(self, req):
        serializer = MovieSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=req.user)
        return Response(serializer.data, 201)
    def get(self, req):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, req)
        serializers = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializers.data)

class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowed]

    def get(self, req, movie_id:int):
        movie = Movie.objects.get(id = movie_id)
        serializers = MovieSerializer(movie)
        return Response(serializers.data)
    def delete(self, req, movie_id:int):
        movie = Movie.objects.get(id=movie_id)
        movie.delete()
        return Response(status=204)

class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, req, movie_id):
        movie = Movie.objects.get(id=movie_id)
        serializers = MovieOrderSerializer(data=req.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(user=req.user, movie=movie)

        return Response(serializers.data, 201)