from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from api import serializers
from rest_framework import viewsets
from api import models
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


class HelloApiView(APIView):

    """Test API view"""
    serializer_class = serializers.HelloSerializer
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
    
    def post(self, request, format=None):
        """Create a hello message with our name"""
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})
        
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    
    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hello {name} !"
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handle updating an object by its ID"""
        return Response({'http_method': 'PUT'})
    def partial_update(self, request, pk=None):
        """Handle partial"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle destroying"""
        return Response({'http_method': 'DELETE'})
    

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating a new user profile"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    # Pour permettre a l'utilisateur de modifier son profile seulement s'il est connecte sur celui ci
    authentication_classes = (TokenAuthentication,) 
    permission_classes = (permissions.UpdateOwnProfile,)

    # Ajouter des filtres en fonction de certains champs
    filter_backends = (filters.SearchFilter,) 
    search_fields = ('name', 'email',)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication Tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,) # Pour definir le type d'authentification
    serializer_class = serializers.ProfileFeedItemSerializer # Pour definir le serializer a appliquer
    queryset = models.ProfileFeedItem.objects.all() # Definition du queryset
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated) # Definition des permissions ..L'utilisateur est authentifie ou n'a que le droit de lecteur des elements de notre api et non le droit d'ecriture

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

