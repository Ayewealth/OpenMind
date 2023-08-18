from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from user.models import *
from .serializers import *

# Create your views here.


@api_view(['Get'])
def endpoints(request):
    data = [
        '/user', '/user:<username>',
        '/instructor', '/instructor:<username>',
        '/courses', '/courses:<title>',
        'reviews', 'reviews:<course>'
        '/blog', '/blog:<title>',
        '/carts', '/cartitems',
    ]
    return Response(data)


# ---------------------------------------------- Users ----------------------------------------------


class UserListCreateApiView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = {
        'name': ['icontains'],
        'username': ['icontains'],
        'email': ['icontains'],
    }


class LoginView(APIView):
    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            response = {
                "message": "Login Successfull",
                "token": user.auth_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }

        return Response(data=content, status=status.HTTP_200_OK)


class UserRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class UserProfileListApiView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = {
        'bio': ['icontains'],
    }


class UserProfileRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

# ------------------------------------------------- Instructor --------------------------------


class InstructorListCreateApiView(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = {
        'name': ['icontains'],
        'username': ['icontains'],
        'email': ['icontains'],
    }


class InstructorRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class InstructorProfileListApiView(generics.ListAPIView):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = {
        'bio': ['icontains'],
        'account_name': ['icontains'],
        # 'user': ['icontains'],
    }


class InstructorProfileRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


# ------------------------------------------------- Courses --------------------------------


class CourseCreateListApiView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = {
        'title': ['icontains'],
        'description': ['icontains'],
    }

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(instructor=user)
        return super().perform_create(serializer)


class CourseRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'title'

    def perform_update(self, serializer):
        instance = serializer.save()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

# ------------------------------------------------- Courses --------------------------------


class ReviewCreateListApiView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# class ReviewRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     lookup_field = 'course'

#     def perform_update(self, serializer):
#         instance = serializer.save()

#     def perform_destroy(self, instance):
#         return super().perform_destroy(instance)

# ----------------------------------------------- Cart------------------------------------------
class CartViewSet(ModelViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer

        elif self.request.method == 'PATCH':
            return UpdateCartItemSerialer

        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
