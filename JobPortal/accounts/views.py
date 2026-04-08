from accounts.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializers = UserRegisterSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message" : "User Registered Successfully.."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email = email)
        except:
            return Response({"error":"Invalid email"},status=status.HTTP_400_BAD_REQUEST)
        
        if not check_password(password, user.password):
            return Response({"error":"Invalid Password"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message":"Login Successfull", 
            "Username":user.first_name,
            "role":user.role
        })

# class LogoutAPIView(APIView):                       # This logout API view for auth_token
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response({"message": "Logout successful"})

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"},status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data) 
    
    def put(self, request):
        serializer = UserRegisterSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

   
    def patch(self, request):
        serializer = UserRegisterSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    
    def delete(self, request):
        request.user.delete()
        return Response(
            {"message": "Your account deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    
class ResumeUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # ✅ Fix role check (adjust field name if needed)
        if request.user.role != 'jobseeker':
            return Response(
                {"error": "Only Jobseekers can upload the resume.."},
                status=status.HTTP_403_FORBIDDEN
            )

        resume, created = Resume.objects.get_or_create(user=request.user)

        serializer = ResumeSerializer(
            resume,
            data=request.data,
            partial=True
        )

        # ✅ MUST call is_valid()
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)