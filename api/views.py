from webbrowser import get
import celery
import os
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, \
    TargetsSerializer, ScansSerializer, OrganizationSerializer, ProjectsSerializer
from projects.models import Targets, Scans, Organization, Projects
from projects.task import dependency_check_tool, check_tool_snyk, check_tool_semgrep, check_tool_checkmarx
from django_celery_results.models import TaskResult
from zipfile import ZipFile
from CheckmarxPythonSDK.config import config
from os.path import normpath, join, dirname, exists
import time
from datetime import datetime

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [permissions.IsAuthenticated]


class TargetsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Targets.objects.all()
    serializer_class = TargetsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path="scan", serializer_class=TargetsSerializer)
    def scan(self, request, pk):
        try:
            # print(pk)
            target_id = Targets.objects.get(pk=pk)
            path = str('./media/') + str(target_id.target_source_code)
            zip_file_path = os.path.abspath(path)
            zf = ZipFile(path, 'r')
            zf.extractall(os.path.dirname(path))
            zf.close()
            source = os.path.splitext(path)[0]
            print(zip_file_path)
            dependency_check_tool.delay(source)
            check_tool_snyk.delay(source)
            check_tool_semgrep.delay(source)
            check_tool_checkmarx.delay(team_full_name="/CxServer",
                                       project_name = os.path.splitext(os.path.basename(zip_file_path))[0] + datetime.now().strftime('_%Y_%m_%d_%H_%M_%S'),
                                       report_type = "XML",
                                       zip_file_path = zip_file_path,
                                       report_folder = config.get("report_folder")
                                       )
            # task_id1 = task1.id
            # task_id2 = task2.id
            # task_id3 = task3.id
            # TaskResult.objects.create(task_id=task_id1)
            # TaskResult.objects.create(task_id=task_id2)
            # TaskResult.objects.create(task_id=task_id3)
        except KeyError:
            raise ParseError('Request has no resource file attached')
        return Response({'status': "1"})


class ScansViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Scans.objects.all()
    serializer_class = ScansSerializer
    permission_classes = [permissions.IsAuthenticated]
