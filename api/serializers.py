from django.contrib.auth.models import User, Group
from rest_framework import serializers

from projects.models import Organization, Projects, Targets, Scans


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"


class TargetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Targets
        fields = "__all__"


class ScansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Targets
        fields = "__all__"


class ScansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scans
        fields = "__all__"
