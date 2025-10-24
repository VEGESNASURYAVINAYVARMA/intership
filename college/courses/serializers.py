# from rest_framework import serializers

# class TopicSerializer(serializers.Serializer):
#     _id = serializers.CharField(read_only=True)
#     title = serializers.CharField(required=True)
#     metadata = serializers.DictField(required=False, default={})
#     module_id = serializers.CharField(required=True)


# class ModuleSerializer(serializers.Serializer):
#     _id = serializers.CharField(read_only=True)
#     title = serializers.CharField(required=True)
#     description = serializers.CharField(required=False, allow_blank=True)
#     metadata = serializers.DictField(required=False, default={})
#     course_id = serializers.CharField(required=True)
#     topic_ids = serializers.ListField(child=serializers.CharField(), required=False)


# # class CourseSerializer(serializers.Serializer):
# #     _id = serializers.CharField(read_only=True)
# #     course_title = serializers.CharField(required=True)
# #     course_description = serializers.CharField(required=True)
# #     course_start_date = serializers.DateTimeField(required=True)
# #     course_end_date = serializers.DateTimeField(required=True)
# #     metadata = serializers.DictField(required=False, default={})
# #     module_ids = serializers.ListField(child=serializers.CharField(), required=False)
# #     display_price = serializers.DictField(required=False)  

# from rest_framework import serializers
# from datetime import datetime

# class CourseSerializer(serializers.Serializer):
#     _id = serializers.CharField(read_only=True)

#     course_title = serializers.CharField(required=True)
#     course_description = serializers.CharField(required=True)
#     course_start_date = serializers.DateTimeField(required=True)
#     course_end_date = serializers.DateTimeField(required=True)

#     metadata = serializers.DictField(required=False, default={})
#     module_ids = serializers.ListField(
#         child=serializers.CharField(), required=False, default=list
#     )

#     # Auto-default fields
#     segment = serializers.CharField(required=False, default="skill_based")
#     course_type = serializers.CharField(required=False, default="single")
#     delivery_mode = serializers.CharField(required=False, default="self_paced")
#     is_locked = serializers.BooleanField(required=False, default=False)
#     image_url = serializers.CharField(
#         required=False,
#         default="https://cdn.synchroni.in/backend/courses-images/converted-webp-images/devops_course.webp",
#     )
#     enrollers = serializers.ListField(required=False, default=list)
#     progress = serializers.FloatField(required=False, default=0)
#     difficulty_level = serializers.CharField(required=False, default="Intermediate")
#     display_price = serializers.DictField(
#         required=False,
#         default=lambda: {"amount": 0, "currency": "INR"}
#     )

#     # Author & timestamps (filled automatically)
#     created_by = serializers.CharField(read_only=True)
#     updated_by = serializers.CharField(read_only=True)
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return validated_data

# class VersionSerializer(serializers.Serializer):
#     versionid = serializers.CharField(required=True)
#     type = serializers.CharField(required=True)
#     title = serializers.CharField(required=True)
#     data = serializers.CharField(allow_null=True, required=False)
#     url = serializers.CharField(allow_null=True, required=False)
#     metadata = serializers.DictField(required=False)

# class ContentSerializer(serializers.Serializer):
#     _id = serializers.CharField(read_only=True)
#     topic_id = serializers.CharField(required=True)
#     version = serializers.DictField(required=True)


# # ----------------- ENROLLMENT -----------------
# class EnrollmentSerializer(serializers.Serializer):
#     _id = serializers.CharField(read_only=True)
#     user_id = serializers.CharField(max_length=100)
#     course_id = serializers.CharField(max_length=100)
#     status = serializers.CharField(max_length=50, default="enrolled")

from rest_framework import serializers

# ----------------- TOPIC -----------------
class TopicSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    metadata = serializers.DictField(required=False, default={})
    module_id = serializers.CharField(required=True)

# ----------------- MODULE -----------------
class ModuleSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.DictField(required=False, default={})
    course_id = serializers.CharField(required=True)
    topic_ids = serializers.ListField(child=serializers.CharField(), required=False, default=list)

# ----------------- COURSE -----------------
class CourseSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    course_title = serializers.CharField(required=True)
    course_description = serializers.CharField(required=True)
    course_start_date = serializers.DateTimeField(required=True)
    course_end_date = serializers.DateTimeField(required=True)
    metadata = serializers.DictField(required=False, default={})
    module_ids = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    segment = serializers.CharField(required=False, default="skill_based")
    course_type = serializers.CharField(required=False, default="single")
    delivery_mode = serializers.CharField(required=False, default="self_paced")
    is_locked = serializers.BooleanField(required=False, default=False)
    image_url = serializers.CharField(required=False, default="https://cdn.synchroni.in/backend/courses-images/converted-webp-images/devops_course.webp")
    enrollers = serializers.ListField(required=False, default=list)
    progress = serializers.FloatField(required=False, default=0)
    difficulty_level = serializers.CharField(required=False, default="Intermediate")
    display_price = serializers.DictField(required=False, default=lambda: {"amount": 0, "currency": "INR"})
    created_by = serializers.CharField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return validated_data

# ----------------- CONTENT -----------------
class VersionSerializer(serializers.Serializer):
    versionid = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    data = serializers.CharField(allow_null=True, required=False)
    url = serializers.CharField(allow_null=True, required=False)
    metadata = serializers.DictField(required=False)

class ContentSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    topic_id = serializers.CharField(required=True)
    version = serializers.DictField(required=True)

# ----------------- ENROLLMENT -----------------
class EnrollmentSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(max_length=100)
    course_id = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=50, default="enrolled")
