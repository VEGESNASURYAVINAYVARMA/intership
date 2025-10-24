from rest_framework import serializers

class QuizOptionSerializer(serializers.Serializer):
    option_text = serializers.CharField()
    is_correct = serializers.BooleanField(default=False)

class QuizContentSerializer(serializers.Serializer):
    question_type = serializers.ChoiceField(choices=["MCQ", "MULTI", "TRUEFALSE", "FILLBLANK", "DESCRIPTIVE"])
    question_text = serializers.CharField()
    question_options = QuizOptionSerializer(many=True, required=False)
    answer_explanation = serializers.CharField(required=False, allow_blank=True)

class QuizSerializer(serializers.Serializer):
    type = serializers.CharField()
    difficulty = serializers.CharField()
    quiz_content = serializers.DictField()
    metadata = serializers.DictField()
    status = serializers.CharField(default="active", required=False)
    points = serializers.IntegerField(default=1, required=False)
    mode = serializers.CharField(default="manual", required=False)
