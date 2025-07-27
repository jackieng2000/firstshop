from rest_framework import serializers
from .models import User, Address
from django.contrib.auth.password_validation import validate_password

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'zip_code', 'is_default']

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'phone_number', 'is_verified', 'addresses', 'password', 'confirm_password']
        read_only_fields = ['is_verified']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'phone_number', 'addresses']
        read_only_fields = ['email', 'id']

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()

        if addresses_data:
            for address_data in addresses_data:
                address_id = address_data.get('id')
                if address_id:
                    address = Address.objects.get(id=address_id, user=instance)
                    for key, value in address_data.items():
                        setattr(address, key, value)
                    address.save()
                else:
                    Address.objects.create(user=instance, **address_data)

        return instance

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data