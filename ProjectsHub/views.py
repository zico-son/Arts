from rest_framework.viewsets import ModelViewSet
from ProjectsHub.serializers import *
from ProjectsHub.models import *

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer