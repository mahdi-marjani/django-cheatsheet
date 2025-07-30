from rest_framework import serializers
from .models import Question, Answer
from .custom_relational_fields import UserEmailNameRelationalField

class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    age = serializers.IntegerField()
    email = serializers.EmailField()

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    # user = serializers.StringRelatedField(read_only=True) # __str__
    # user = serializers.PrimaryKeyRelatedField(read_only=True) # pk (default)
    # user = serializers.SlugRelatedField(read_only=True, slug_field='email') # Optional field
    user = UserEmailNameRelationalField(read_only=True) # custom relational field (Rarely used)

    class Meta:
        model = Question
        fields = '__all__'
    
    def get_answers(self, obj):
        result = obj.answers.all()
        return AnswerSerializer(instance=result, many=True).data

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'