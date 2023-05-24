from django.urls import path
from Core.views import *

urlpatterns = [
    path ('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path ('register/', RegisterUsersViewSet.as_view({'post': 'create'}), name='register'),
]
