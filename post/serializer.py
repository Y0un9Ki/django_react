from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Post
        fields = ['user', 'title', 'content', 'created_at']
        
    def validate(self, attrs):
        if len(attrs.get('title', ''))>100:
            raise serializers.ValidationError({'message': 'title이 100글자를 넘지 않게 해주세요'})
        if len(attrs.get('content', ''))>500:
            raise serializers.ValidationError({'message' : '내용이 너무 길어요. 500글자 미만으로 작성해주세요'})
        return attrs
    
    # def create(self, validated_data):
    #     return Post.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.content = validated_data.get('content', instance.content)
        
    #     instance.save()
    #     return instance