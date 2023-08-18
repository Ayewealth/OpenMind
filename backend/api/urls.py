from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = DefaultRouter()
router.register('cart', views.CartViewSet)

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup="cart")
cart_router.register('items', views.CartItemViewSet, basename="cart_items")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),

    path('', views.endpoints),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --------------------------------------- User information --------------------------------

    path('users', views.UserListCreateApiView.as_view()),
    path('users/<str:username>/',
         views.UserRetrieveUpdateDestroyApiView.as_view(), name='user_detail'),
    path('login', views.LoginView.as_view()),

    path('users-profile', views.UserProfileListApiView.as_view(), name='user_profile'),
    path('users-profile/<str:pk>/',
         views.UserProfileRetrieveUpdateDestroyApiView.as_view(), name='user_profile_details'),

    # -------------------------------------------- Instructor information --------------------------------

    path('instructors', views.InstructorListCreateApiView.as_view()),
    path('instructors/<str:username>/',
         views.InstructorRetrieveUpdateDestroyApiView.as_view(), name='instructor_detail'),

    path('instructors-profile', views.InstructorProfileListApiView.as_view(),
         name='instructor_profile'),
    path('instructors-profile/<str:pk>/',
         views.InstructorProfileRetrieveUpdateDestroyApiView.as_view(), name='instructor_profile_details'),

    # -------------------------------------------- Instructor information --------------------------------

    path('courses', views.CourseCreateListApiView.as_view()),
    path('courses/<str:title>/', views.CourseRetrieveUpdateDestroyApiView.as_view()),

    # -------------------------------------------- Instructor information --------------------------------

    path('reviews', views.ReviewCreateListApiView.as_view()),
    #     path('reviews/<str:course>/',
    #          views.ReviewRetrieveUpdateDestroyApiView.as_view())

    # -------------------------------------------- Cart ------------------------------------------------
    #     path('cart', views.CartCreateApiView.as_view()),
    #     path('cart/<str:pk>/', views.CartRetrieveUpdateDeleteApiView.as_view(), name="carts"),
]
