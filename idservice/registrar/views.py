import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import ObjectID
from .permissions import AuthenticatedAndGroupMember
from .serializers import UserSerializer, GroupSerializer, ObjectIDSerializer

from DDR import identifier


@api_view(['GET'])
def index(request):
    url = reverse('api-root')
    url = '/api/0.1/'
    return HttpResponseRedirect(url)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'groups': reverse('group-list', request=request, format=format),
        'objectids': reverse('objectid-list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class ObjectIDViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ObjectID to be viewed or edited.
    """
    queryset = ObjectID.objects.all()
    serializer_class = ObjectIDSerializer
    permission_classes = (
        AuthenticatedAndGroupMember,
    )


@api_view(['GET', 'POST'])
def next_object(request, oid, model):
    oi = identifier.Identifier(oid)
    
    if model not in oi.child_models(stubs=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if not identifier.Identifier.nextable(model):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    next_object = ObjectID.next(oi, model)
    
    serializer = ObjectIDSerializer(
        data={
            'url': next_object.absolute_url(),
            'id': next_object.id,
            'model': next_object.model,
            'group': next_object.group,
        },
        context={'request': request}
    )
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    data = {
        'url': next_object.absolute_url(),
        'id': next_object.id,
        'model': next_object.model,
        'group': next_object.group.name,
    }
    
    if request.method == 'GET':
        #return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if not (
            request.user.is_staff or (next_object.group in request.user.groups)
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        next_object.save()
        #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_201_CREATED)
