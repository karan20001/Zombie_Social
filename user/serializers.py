from rest_framework import serializers
from .models import User,InventoryDetails

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'name', 'email', 'password','lat', 'long']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLocationSerializer(serializers.Serializer):
    lat = serializers.DecimalField(max_digits=15, decimal_places=10)
    long = serializers.DecimalField(max_digits=15, decimal_places=10)
