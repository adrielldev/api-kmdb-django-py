from rest_framework.permissions import IsAdminUser
from .permissions import IsUserOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from .serializers import UserSerializer
from .models import User



class AllUserView(APIView,PageNumberPagination):
    permission_classes = [IsAdminUser]
    def get(self,request):
       users = User.objects.all()
       result_page = self.paginate_queryset(users, request, view=self)
       users_json = UserSerializer(result_page,many=True)

       return self.get_paginated_response(users_json.data)

class UserView(APIView):
    permission_classes = [IsUserOwner]
    def get(self,request,id):
        user = User.objects.get(pk=id)
        
        self.check_object_permissions(request,user)
        
        user_serializer = UserSerializer(user)
        
        return Response(user_serializer.data)

class UserRegisterView(APIView):
    def post(self,request):
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response(user.data,status.HTTP_201_CREATED)



