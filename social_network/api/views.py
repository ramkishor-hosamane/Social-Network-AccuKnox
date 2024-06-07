
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from api.throttles import FriendRequestThrottle
from .models import FriendRequest
from rest_framework import serializers
from .serializers import LoginSerializer, SignUpSerializer, UserSerializer, FriendRequestSerializer
from rest_framework.pagination import PageNumberPagination
User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.filter(email__iexact=email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'detail': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class FriendListPagination(PageNumberPagination):
    page_size = 10
    # page_size_query_param = 'page_size'
    # max_page_size = 100

class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = FriendListPagination 
    def get_queryset(self):
        queryset = User.objects.all()
        query = self.request.query_params.get('query', None)
        if query:
            if '@' in query:
                queryset = queryset.filter(email__iexact=query)
            else:
                queryset = queryset.filter(name__icontains=query)
        return queryset



class FriendRequestCreateAPIView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    throttle_classes = [FriendRequestThrottle]

    def perform_create(self, serializer):
        from_user = self.request.user
        to_user_id = self.request.data.get('to_user_id')
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Friend request : The user does not exist')
        if from_user == to_user:
            raise serializers.ValidationError('You cannot Send Friend request to yourself')

        
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
            raise serializers.ValidationError('Friend request already sent')
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='accepted').exists():
            raise serializers.ValidationError('The user is already your friend')

        if FriendRequest.objects.filter(from_user=to_user,to_user= from_user, status='accepted').exists():
            raise serializers.ValidationError('The user is already your friend')
                
        if FriendRequest.objects.filter(from_user=to_user,to_user= from_user, status='pending').exists():
            raise serializers.ValidationError('You already have request from this User')        
        
        serializer.save(from_user=from_user, to_user=to_user)

class FriendRequestListAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')




class FriendListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__to_user=self.request.user, sent_requests__status='accepted') |
            Q(received_requests__from_user=self.request.user, received_requests__status='accepted')
        ).distinct()


class FriendRequestUpdateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        friend_request_id = self.kwargs['pk']
        action = self.request.data.get('action')
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user,status="pending")
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Invalid Friend Request'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'status': 'accepted'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'status': 'rejected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)