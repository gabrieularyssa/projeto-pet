from pickletools import read_floatnl
from sre_constants import SRE_INFO_LITERAL
from rest_framework import serializers


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length=20)
    scientific_name = serializers.CharField(max_length=50)
    
