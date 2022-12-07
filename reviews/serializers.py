from rest_framework.serializers import ModelSerializer
from .models import Review

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    
    def create(self,validated_data:dict):
        review = Review.objects.create(**validated_data)

        return review
        
