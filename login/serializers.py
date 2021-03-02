from rest_framework import serializers



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class ForGetPassWordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try :
            user = User.objects.get(email = data['email'])
        except :
            raise serializers.ValidationError("use email does not existed.")
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