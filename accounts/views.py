from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (UserSignupSerializer, UserLoginSerializer, 
                          UserProfileSerializer, PasswordResetRequestSerializer, PasswordResetSerializer,
                          PasswordChangeSerializer)
from .token_auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import UserProfile, CustomUser
from django.shortcuts import get_object_or_404

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve and update the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override the get_object method to return the profile of the authenticated user.
        """
        return get_object_or_404(UserProfile, user=self.request.user)


class UserSignupView(APIView):
    """
    API endpoint for user signup.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new user.

        Parameters:
        - request: The HTTP request object containing the user's data.

        Returns:
        - A JSON response containing the created user's information or validation errors.
        """
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user": {
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    API endpoint for user login.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to authenticate a user and return a JWT.
        
        Returns:
        - A JSON response containing the JWT, user details, and user profile if authentication is successful.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = TokenAuthentication.generate_jwt(user)

            # Get the user's profile (assuming there's a OneToOne relationship)
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                user_profile = None

            # Serialize the user profile
            profile_serializer = UserProfileSerializer(user_profile)

            return Response({
                'token': token,
                'profile': profile_serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DummyView(APIView):
    """
    A dummy view to test Bearer token authentication.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and returns a success message if the user is authenticated.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A JSON response containing a success message.
        """
        return Response({'message': 'Authenticated successfully!'}, status=status.HTTP_200_OK)
    


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve and update the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override the get_object method to return the profile of the authenticated user.
        """
        return get_object_or_404(UserProfile, user=self.request.user)
    


class PasswordResetRequestView(generics.CreateAPIView):
    """
    Handles the request to send a password reset OTP to the user's email.
    """
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "OTP has been sent to your email."}, status=status.HTTP_200_OK)

class PasswordResetView(generics.CreateAPIView):
    """
    Handles the request to reset the password using the OTP.
    """
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Your password has been reset successfully."}, status=status.HTTP_200_OK)



class PasswordChangeView(generics.UpdateAPIView):
    """
    An endpoint for the user to change their password.
    """
    serializer_class = PasswordChangeSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        """
        Retrieve and return the authenticated user.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Handle the PUT request to change the user's password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
