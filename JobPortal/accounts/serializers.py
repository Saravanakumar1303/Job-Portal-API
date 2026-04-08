from rest_framework import serializers
from accounts.models import User,Resume
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields =["id","first_name","last_name","email","username","password","role","profile_photo"]
            read_only_fileds = ["id"]
            extra_kwargs ={
                "password":{"write_only":True}
            }
    
        def create(self, validated_data):
            return User.objects.create_user(**validated_data) #create_user() automation changed the password form

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            email = data["email"],
            password = data["password"]
        )
        if not user:
            raise serializers.ValidationError("Invalid Username and Password...")
        data["user"] = user
        return data
    
class ResumeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Resume 
          fields = ['resume','skills','experience']


class ProfileSerializer(serializers.ModelSerializer):
    resume = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email','role', 'profile_photo','resume']

    def get_resume(self, obj):
        resume = Resume.objects.filter(user=obj).first()
        if resume:
            return ResumeSerializer(resume).data
        return None
