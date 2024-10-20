from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from .permissions import IsAdmin  

class UserCreateView(generics.CreateAPIView):
    """Представление для создания пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserLoginView(generics.GenericAPIView):
    """Представление для логина пользователя."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')

        user = authenticate(request, login=login, password=password)

        if user is not None:
            token = AccessToken.for_user(user)
            response = Response(
                {
                    'id': user.id,
                    'role': user.role,
                    'token': str(token)
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie(key='jwt', value=str(token), httponly=True)  
            return response
        else:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin] 

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]  
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)