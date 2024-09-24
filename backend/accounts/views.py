from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSignupSerializer, UserLoginSerializer
from .token_auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
        
        Parameters:
        - request: The HTTP request object containing the user's credentials.
        
        Returns:
        - A JSON response containing the JWT if authentication is successful, or errors if not.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = TokenAuthentication.generate_jwt(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
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