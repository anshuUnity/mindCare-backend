from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import UserProfile, PasswordResetOTP
import random
from .Utils import send_email
from django.contrib.auth import password_validation

CustomUser = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate(self, data):
        """
        Validate and sanitize the data.
        """
        email = data.get('email', None)
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return data

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        Validate the login credentials.
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        data['user'] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'gender', 'phone_number', 'profile_picture', 'bio']
        read_only_fields = ['user']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        otp = f"{random.randint(100000, 999999)}"

        # Send the OTP via email
        # For demonstration purposes, we'll use Django's email backend
        # In production, use a proper email service

        status = send_email(
            subject="Mindcare Password Reset OTP",
            message=f"Your OTP for password reset is: {otp}",
            recipient_list=[email]
        )
        if status == 1:
            PasswordResetOTP.objects.create(user=user, otp=otp)



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")

        try:
            otp_record = PasswordResetOTP.objects.get(user=user, otp=data['otp'], is_used=False)
        except PasswordResetOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")

        # Check if OTP has expired (optional, e.g., valid for 10 minutes)
        # if timezone.now() > otp_record.created_at + timedelta(minutes=10):
        #     raise serializers.ValidationError("OTP has expired.")

        data['user'] = user
        data['otp_record'] = otp_record
        return data

    def save(self):
        user = self.validated_data['user']
        otp_record = self.validated_data['otp_record']
        new_password = self.validated_data['new_password']

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Mark the OTP as used
        otp_record.is_used = True
        otp_record.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        """
        Check that the new password and confirm password match.
        """
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("The two new passwords do not match.")
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError("Old and New Password are same")
        return data

    def validate_new_password(self, value):
        """
        Validate the new password against Django's built-in password validators.
        """
        password_validation.validate_password(value, self.context['request'].user)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


