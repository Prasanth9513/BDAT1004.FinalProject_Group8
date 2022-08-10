from rest_framework import serializers
from .models import *






class ExchangeSerializer(serializers.ModelSerializer):
    #upload_documents = serializers.FileField(max_length=None, use_url=True)
    class  Meta:
          model        =           Exchange
          fields       =           '__all__'
