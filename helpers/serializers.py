from rest_framework import serializers

from helpers.models import Question, QuestionCategory, Callback, PolicyConf


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionCategorySerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionCategory
        fields = ['id', 'title', 'question']


class CallbackSerializer(serializers.ModelSerializer):
    checked = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Callback
        fields = '__all__'


class PolicyConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyConf
        fields = '__all__'
