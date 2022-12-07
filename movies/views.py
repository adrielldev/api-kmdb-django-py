from reviews.serializers import ReviewSerializer
from .serializers import MovieSerializer
from rest_framework.views import APIView
from .models import Movie
from rest_framework.response import Response
from .permissions import IsCriticOrIsAdmPermission, IsReviewOwner, MoviePermission
from rest_framework import status
from reviews.models import Review
from users.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView,PageNumberPagination):
    permission_classes = [MoviePermission]
    def get(self,request): 

        all_movies = Movie.objects.all()
        result_page = self.paginate_queryset(all_movies, request, view=self)
        movies_json = MovieSerializer(result_page,many=True)

        return self.get_paginated_response(movies_json.data)

    def post(self,request):

        movie = MovieSerializer(data=request.data)
        movie.is_valid(raise_exception=True)
        movie.save()

        return Response(movie.data,status.HTTP_201_CREATED)

class MovieIdView(APIView):
    permission_classes = [MoviePermission]
    def get(self,request,id):
        try:
            movie = Movie.objects.get(pk=id)
            movie_data = MovieSerializer(movie)
            return Response(movie_data.data)
        except Movie.DoesNotExist:
            return Response({"detail":'Movie not found'},status.HTTP_404_NOT_FOUND)
        

    def delete(self,request,id):
        try:
            movie = Movie.objects.get(pk=id)
            movie.delete()
        except Movie.DoesNotExist:
            return Response({"detail":'Movie not found'},status.HTTP_404_NOT_FOUND)
        return Response({},status.HTTP_204_NO_CONTENT)

    def patch(self,request,id):
        try:
            movie = Movie.objects.get(pk=id)
            movie_data = MovieSerializer(movie,request.data,partial=True)
            movie_data.is_valid()
            movie_data.save()
            

            return Response(movie_data.data)
        except Movie.DoesNotExist:
            return Response({"detail":'Movie not found'},status.HTTP_404_NOT_FOUND)


class MovieReviews(APIView,PageNumberPagination):
    permission_classes = [IsCriticOrIsAdmPermission]
    def post(self,request,id):
        user = UserSerializer(request.user)
        movie = Movie.objects.get(pk=id)
        movie_serializer = MovieSerializer(movie)
        reviews = Review.objects.filter(movie_id=id,user_id=request.user.id)
        if len(reviews) > 0:
           return Response({"detail": "Review already exists."},status.HTTP_403_FORBIDDEN)

        review_serializer = ReviewSerializer(data={**request.data,"user":user.data['id'],"movie":movie_serializer.data['id']})
        review_serializer.is_valid(raise_exception = True)
        review_serializer.save()
        review_serializer.data.popitem()
        review_data = {}
        for key,value in review_serializer.data.items():
            if key != 'user' and key != 'movie':
                review_data[key] = value
        review_data['movie_id'] = review_serializer.data['movie']
        review_data['critic'] = {
            "id":user.data['id'],
            "first_name":user.data['first_name'],
            "last_name":user.data['last_name']
        }
        return Response(review_data,status.HTTP_201_CREATED)

    def get(self,request,id):
        reviews = Review.objects.filter(movie_id=id)
        result_page = self.paginate_queryset(reviews, request, view=self)
        reviews_serializer = ReviewSerializer(result_page,many=True)
        return self.get_paginated_response(reviews_serializer.data)


class MovieIdReviews(APIView):
    
    permission_classes = [IsReviewOwner]
    def get(self,request,id_movie,id_review):
        try:
            reviews = Review.objects.filter(movie_id=id_movie)
            reviews_serializer = ReviewSerializer(reviews,many=True)
            for review in reviews_serializer.data:
                if review['id'] == id_review:
                    review_data = review

            return Response(review_data)
        except Review.DoesNotExist:
            return Response({"detail":'Review not found'},status.HTTP_404_NOT_FOUND)
        

    def delete(self,request,id_movie,id_review):
        try:
            review = Review.objects.get(pk=id_review)
            self.check_object_permissions(request,review)
            review.delete()

            return Response({},status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({"detail":'Review not found'},status.HTTP_404_NOT_FOUND)