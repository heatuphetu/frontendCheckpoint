
from django.contrib import admin
from django.urls import path
from myapp.views import RegisterView, LoginView, UserDetailView, SellerCreateView, BookCreateView, BookListView, SellerDetailView, UserBooksView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/auth/register',RegisterView.as_view(), name = "auth_register"),
        path('api/auth/login', LoginView.as_view(), name="auth_login"),

        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

        path('api/auth/user', UserDetailView.as_view(), name="auth_user"),
        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('api/sellers/', SellerCreateView.as_view(), name='seller_create'),
        path('api/books/', BookCreateView.as_view(), name='book_create'),
        path('api/books/list/', BookListView.as_view(), name='book_list'),

        path('api/sellers/detail/', SellerDetailView.as_view(), name='seller_detail'),

        path('api/user/books', UserBooksView.as_view(), name="user_books"),

]
