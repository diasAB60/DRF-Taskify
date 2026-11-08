

from .models import (
    User, UserProfile,
    Organization, OrganizationMember,
    Project, Task)

from rest_framework import status, viewsets, generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


from .serializers import (
    UserSerializer, UserProfileSerializer,
    OrganizationSerializer, OrganizationMemberSerializer,
    ProjectSerializer, TaskSerializer,
    RegisterSerializer)


@extend_schema(
    request=RegisterSerializer,  # Указываем, какой сериализатор ожидает на вход
    responses={201: RegisterSerializer} # (опционально) схема ответа
)

class RegisterView(APIView):
    permission_classes =[AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes =[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.user_profile


class OrganizationViewSet(viewsets.ModelViewSet):

    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        organization = serializer.save(creator=self.request.user)

        OrganizationMember.objects.create(
            user = self.request.user,
            organization = organization,
            role = 'admin'
        )


class OrganizationMemberViewSet(viewsets.ModelViewSet):

    serializer_class = OrganizationMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrganizationMember.objects.filter(organization__members=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(organization__members=self.request.user)

    def perform_create(self, serializer):
        organization = serializer.validated_data['organization']

        if not organization.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You cannot create a project in this organization.")

        serializer.save()


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__organization__members=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data['project']

        if not project.organization.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You cannot create a task in this project.")

        serializer.save(creator=self.request.user)




