from django.contrib.auth.models import User

from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def create(self, validated_data):
        print('validated_data is =>', validated_data)
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class ForGetPassWordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try :
            user = User.objects.get(email = data.get('email'))
        except :
            raise serializers.ValidationError("user email does not existed.")
        
        return data


class ResetPassWordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ('email', 'password',)