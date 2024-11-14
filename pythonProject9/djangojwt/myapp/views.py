from django.contrib.auth import authenticate
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Seller, Book
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, SellerSerializer, BookSerializer
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


class SellerCreateView(generics.CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the user only has one seller
        if not Seller.objects.filter(user=self.request.user).exists():
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("You can only create one seller.")


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Get the seller associated with the current user
            seller = Seller.objects.get(user=self.request.user)
            serializer.save(seller=seller)
        except Seller.DoesNotExist:
            return Response(
                {"error": "No seller found for the logged-in user. Please create a seller first."},
                status=status.HTTP_400_BAD_REQUEST
            )


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow public access to book list

class SellerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            seller = Seller.objects.get(user=request.user)
            serializer = SellerSerializer(seller)
            return Response(serializer.data)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=404)


class UserBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_queryset(self):
        # Return books related to the logged-in user
        user = self.request.user
        try:
            seller = Seller.objects.get(user=user)
            return Book.objects.filter(seller=seller)
        except Seller.DoesNotExist:
            return Book.objects.none()  # Return no books if the user doesn't have a seller profile
