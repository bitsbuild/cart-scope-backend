from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer,CharField,ValidationError
class UserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','confirm_password']
        extra_kwargs = {
            "password":{'write_only':True},
        }
    def validate(self,data):
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError("Username Exists Already!")
        elif data['password'] != data['confirm_password']:
            raise ValidationError("Passwords Do Not Match")
        elif User.objects.filter(password=data['password']).exists():
            raise ValidationError("Existing Account Connected To This Mail ID")
        else:
            return data
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user