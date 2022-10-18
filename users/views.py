from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import RegisterUserSerializer, UserSerializer
from rest_framework.response import Response


User = get_user_model()

class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({
                'status': 'success',
                'data': serializer.data
            })

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data
                
            }, status=201)    
        return Response({
                'status': 'fail',
                'data': {
                    'errors': serializer.errors
                }
            }, status=400)       