# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .mongo_utils import get_db_handle
# from bson import ObjectId
# from .serializers import CourseSerializer, ModuleSerializer, EnrollmentSerializer,TopicSerializer

# db = get_db_handle()
# courses_collection = db["courses"]
# enrollments_collection = db["enrollments"]
# modules_collection = db["modules"]
# topics_collection = db["topics"]


# # -------------------------------------------------------
# # COURSE CRUD
# # -------------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from bson import ObjectId
# from bson.errors import InvalidId
# from .mongo_utils import get_db_handle,convert_objectid
# from .serializers import (
#     CourseSerializer,
#     ModuleSerializer,
#     TopicSerializer,
#     ContentSerializer,
#     EnrollmentSerializer
# )
# from .utils import update_user_progress
# from users.models import User 

# db = get_db_handle()
# courses_collection = db["courses"]
# modules_collection = db["modules"]
# topics_collection = db["topics"]
# contents_collection = db["content"]
# enrollments_collection = db["enrollments"]
# user_progress_collection = db["user_progress"]

# # Helper to convert ObjectId to JSON
# from bson import ObjectId

# def convert_objectid(data):
#     """Recursively convert ObjectIds to strings."""
#     if isinstance(data, list):
#         return [convert_objectid(i) for i in data]
#     if isinstance(data, dict):
#         return {k: convert_objectid(v) for k, v in data.items()}
#     if isinstance(data, ObjectId):
#         return str(data)
#     return data




# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from datetime import datetime

# class CourseView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     # CREATE COURSE
#     def post(self, request):
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             course_data = dict(serializer.validated_data)

#             # Attach logged-in user info
#             course_data["created_by"] = str(request.user.username)
#             course_data["updated_by"] = str(request.user.username)
#             course_data["created_at"] = datetime.utcnow().isoformat() + "Z"
#             course_data["updated_at"] = datetime.utcnow().isoformat() + "Z"

#             # Insert into MongoDB
#             result = courses_collection.insert_one(course_data)
#             course_data["_id"] = result.inserted_id

#             return Response(convert_objectid(course_data), status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # GET ALL COURSES
#     def get(self, request):
#         courses = list(courses_collection.find())
#         for course in courses:
#             module_list = list(modules_collection.find({"_id": {"$in": course.get("module_ids", [])}}))
#             for module in module_list:
#                 topic_list = list(topics_collection.find({"_id": {"$in": module.get("topic_ids", [])}}))
#                 for topic in topic_list:
#                     content_list = list(contents_collection.find({"_id": {"$in": topic.get("content_ids", [])}}))
#                     topic["contents"] = content_list
#                 module["topics"] = topic_list
#             course["modules"] = module_list
#         return Response(convert_objectid(courses), status=status.HTTP_200_OK)



# # COURSE DETAIL VIEW
# class CourseDetailView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, course_id):
#         try:
#             course = courses_collection.find_one({"_id": ObjectId(course_id)})
#         except InvalidId:
#             return Response({"error": "Invalid course_id"}, status=status.HTTP_400_BAD_REQUEST)

#         if not course:
#             return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

#         expanded_modules = []
#         for mid in course.get("module_ids", []):
#             module = modules_collection.find_one({"_id": ObjectId(mid)})
#             if module:
#                 expanded_topics = []
#                 for tid in module.get("topic_ids", []):
#                     topic = topics_collection.find_one({"_id": ObjectId(tid)})
#                     if topic:
#                         expanded_topics.append(topic)
#                 module["topics"] = expanded_topics
#                 expanded_modules.append(module)

#         course["modules"] = expanded_modules
#         return Response(convert_objectid(course), status=status.HTTP_200_OK)

#     def put(self, request, course_id):
#         serializer = CourseSerializer(data=request.data, partial=True)
#         if serializer.is_valid():
#             update_data = serializer.validated_data
#             update_data["updated_by"] = str(request.user.username)
#             update_data["updated_at"] = datetime.utcnow().isoformat() + "Z"

#             result = courses_collection.update_one(
#                 {"_id": ObjectId(course_id)},
#                 {"$set": update_data}
#             )

#             if result.matched_count == 0:
#                 return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

#             course = courses_collection.find_one({"_id": ObjectId(course_id)})
#             return Response(convert_objectid(course), status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # -------------------------------------------------------
# # MODULE CRUD
# # -------------------------------------------------------
# class ModuleView(APIView):
#     def post(self, request):
#         serializer = ModuleSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         module_data = serializer.validated_data
#         course_id = module_data.get("course_id")
#         try:
#             course_objid = ObjectId(course_id)
#         except InvalidId:
#             return Response({"error": "Invalid course_id"}, status=status.HTTP_400_BAD_REQUEST)

#         course = courses_collection.find_one({"_id": course_objid})
#         if not course:
#             return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

#         module_to_insert = {k: v for k, v in module_data.items() if k != "course_id"}
#         module_to_insert.setdefault("topic_ids", [])
#         result = modules_collection.insert_one(module_to_insert)
#         inserted_objid = result.inserted_id

#         courses_collection.update_one(
#             {"_id": course_objid},
#             {"$push": {"module_ids": inserted_objid}}
#         )

#         module_to_insert["_id"] = inserted_objid
#         return Response( convert_objectid(module_to_insert), status=status.HTTP_201_CREATED)

#     def get(self, request):
#         modules = list(modules_collection.find())
#         for module in modules:
#             topic_list = list(topics_collection.find({"_id": {"$in": module.get("topic_ids", [])}}))
#             for topic in topic_list:
#                 content_list = list(contents_collection.find({"_id": {"$in": topic.get("content_ids", [])}}))
#                 topic["contents"] = content_list
#             module["topics"] = topic_list
#         return Response( convert_objectid(modules), status=status.HTTP_200_OK)

# # -------------------------------------------------------
# # TOPIC CRUD
# # -------------------------------------------------------
# class TopicView(APIView):
#     def get(self, request):
#         topics = list(topics_collection.find())
#         return Response( convert_objectid(topics), status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = TopicSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         topic_data = serializer.validated_data
#         module_id = topic_data.get("module_id")
#         try:
#             module_objid = ObjectId(module_id)
#         except InvalidId:
#             return Response({"error": "Invalid module_id"}, status=status.HTTP_400_BAD_REQUEST)

#         module = modules_collection.find_one({"_id": module_objid})
#         if not module:
#             return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

#         topic_to_insert = {k: v for k, v in topic_data.items() if k != "module_id"}
#         result = topics_collection.insert_one(topic_to_insert)
#         new_topic_id = result.inserted_id

#         modules_collection.update_one(
#             {"_id": module_objid},
#             {"$push": {"topic_ids": new_topic_id}}
#         )

#         inserted_topic = topics_collection.find_one({"_id": new_topic_id})
#         return Response( convert_objectid(inserted_topic), status=status.HTTP_201_CREATED)

# class TopicDetailView(APIView):
#     def get(self, request, topic_id):
#         try:
#             topic_objid = ObjectId(topic_id)
#         except InvalidId:
#             return Response({"error": "Invalid topic_id"}, status=status.HTTP_400_BAD_REQUEST)

#         topic = topics_collection.find_one({"_id": topic_objid})
#         if not topic:
#             return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

#         return Response( convert_objectid(topic), status=status.HTTP_200_OK)

#     def put(self, request, topic_id):
#         try:
#             topic_objid = ObjectId(topic_id)
#         except InvalidId:
#             return Response({"error": "Invalid topic_id"}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = TopicSerializer(data=request.data, partial=True)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         update_data = serializer.validated_data
#         result = topics_collection.update_one({"_id": topic_objid}, {"$set": update_data})
#         if result.matched_count == 0:
#             return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

#         updated_topic = topics_collection.find_one({"_id": topic_objid})
#         return Response( convert_objectid(updated_topic), status=status.HTTP_200_OK)

#     def delete(self, request, topic_id):
#         try:
#             topic_objid = ObjectId(topic_id)
#         except InvalidId:
#             return Response({"error": "Invalid topic_id"}, status=status.HTTP_400_BAD_REQUEST)

#         result = topics_collection.delete_one({"_id": topic_objid})
#         if result.deleted_count == 0:
#             return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

#         modules_collection.update_many({}, {"$pull": {"topic_ids": topic_objid}})
#         return Response({"message": "Topic deleted successfully"}, status=status.HTTP_200_OK)

# # -------------------------------------------------------
# # CONTENT CRUD
# # -------------------------------------------------------
# class ContentView(APIView):
#     def post(self, request):
#         serializer = ContentSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         content_data = serializer.validated_data
#         topic_id = content_data.get("topic_id")

#         # Validate topic_id
#         try:
#             topic_objid = ObjectId(topic_id)
#         except InvalidId:
#             return Response({"error": "Invalid topic_id"}, status=status.HTTP_400_BAD_REQUEST)

#         topic = topics_collection.find_one({"_id": topic_objid})
#         if not topic:
#             return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Remove topic_id before insert
#         content_to_insert = {
#             "version": content_data["version"]  # store single version only
#         }

#         result = contents_collection.insert_one(content_to_insert)
#         inserted_id = result.inserted_id

#         # Push content ID into topic
#         topics_collection.update_one(
#             {"_id": topic_objid},
#             {"$push": {"content_ids": inserted_id}}
#         )

#         # Prepare response
#         content_to_insert["_id"] = str(inserted_id)
#         return Response(content_to_insert, status=status.HTTP_201_CREATED)




# class UpdateUserProgressView(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#             user_id = data.get("user_id")
#             course_id = data.get("course_id")
#             module_id = data.get("module_id")
#             topic_id = data.get("topic_id")
#             content_id = data.get("content_id")

#             if not all([user_id, course_id, module_id, topic_id, content_id]):
#                 return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

#             result = update_user_progress(user_id, course_id, module_id, topic_id, content_id)
#             return Response(result, status=status.HTTP_200_OK)

#         except ValueError as e:
#             return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# # -------------------------------------------------------
# # ENROLLMENT CRUD
# # -------------------------------------------------------
# class EnrollmentCreateView(APIView):
#     def post(self, request):
#         serializer = EnrollmentSerializer(data=request.data)
#         if serializer.is_valid():
#             result = enrollments_collection.insert_one(serializer.validated_data)
#             data = serializer.validated_data
#             data["_id"] = result.inserted_id
#             return Response( convert_objectid(data), status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EnrollmentListView(APIView):
#     def get(self, request):
#         enrollments = list(enrollments_collection.find())
#         return Response( convert_objectid(enrollments), status=status.HTTP_200_OK)

# class EnrollmentUpdateView(APIView):
#     def put(self, request, enrollment_id):
#         serializer = EnrollmentSerializer(data=request.data)
#         if serializer.is_valid():
#             result = enrollments_collection.update_one(
#                 {"_id": ObjectId(enrollment_id)},
#                 {"$set": serializer.validated_data}
#             )
#             if result.matched_count == 0:
#                 return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)
#             data = serializer.validated_data
#             data["_id"] = enrollment_id
#             return Response( convert_objectid(data))
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EnrollmentDeleteView(APIView):
#     def delete(self, request, enrollment_id):
#         result = enrollments_collection.delete_one({"_id": ObjectId(enrollment_id)})
#         if result.deleted_count == 0:
#             return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)
#         return Response({"message": "Enrollment deleted"}, status=status.HTTP_204_NO_CONTENT)
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from .mongo_utils import get_db_handle
from .serializers import (
    CourseSerializer,
    ModuleSerializer,
    TopicSerializer,
    ContentSerializer,
    EnrollmentSerializer
)
from .utils import update_user_progress
from users.models import User

# ----------------- MongoDB collections -----------------
db = get_db_handle()
courses_collection = db["courses"]
modules_collection = db["modules"]
topics_collection = db["topics"]
contents_collection = db["content"]
enrollments_collection = db["enrollments"]
user_progress_collection = db["user_progress"]

# ----------------- Helpers -----------------
def convert_objectid(data):
    """Recursively convert ObjectIds to strings."""
    if isinstance(data, list):
        return [convert_objectid(i) for i in data]
    if isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data

# ----------------- COURSE CRUD -----------------
class CourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course_data = dict(serializer.validated_data)
            course_data.update({
                "created_by": str(request.user.username),
                "updated_by": str(request.user.username),
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z"
            })
            result = courses_collection.insert_one(course_data)
            course_data["_id"] = result.inserted_id
            return Response(convert_objectid(course_data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        courses = list(courses_collection.find())
        for course in courses:
            module_list = list(modules_collection.find({"_id": {"$in": course.get("module_ids", [])}}))
            for module in module_list:
                topic_list = list(topics_collection.find({"_id": {"$in": module.get("topic_ids", [])}}))
                for topic in topic_list:
                    content_list = list(contents_collection.find({"_id": {"$in": topic.get("content_ids", [])}}))
                    topic["contents"] = content_list
                module["topics"] = topic_list
            course["modules"] = module_list
        return Response(convert_objectid(courses), status=status.HTTP_200_OK)

class CourseDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = courses_collection.find_one({"_id": ObjectId(course_id)})
        except InvalidId:
            return Response({"error": "Invalid course_id"}, status=status.HTTP_400_BAD_REQUEST)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        expanded_modules = []
        for mid in course.get("module_ids", []):
            module = modules_collection.find_one({"_id": ObjectId(mid)})
            if module:
                expanded_topics = []
                for tid in module.get("topic_ids", []):
                    topic = topics_collection.find_one({"_id": ObjectId(tid)})
                    if topic:
                        expanded_topics.append(topic)
                module["topics"] = expanded_topics
                expanded_modules.append(module)

        course["modules"] = expanded_modules
        return Response(convert_objectid(course), status=status.HTTP_200_OK)

    def put(self, request, course_id):
        serializer = CourseSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            update_data = serializer.validated_data
            update_data.update({
                "updated_by": str(request.user.username),
                "updated_at": datetime.utcnow().isoformat() + "Z"
            })
            result = courses_collection.update_one({"_id": ObjectId(course_id)}, {"$set": update_data})
            if result.matched_count == 0:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            course = courses_collection.find_one({"_id": ObjectId(course_id)})
            return Response(convert_objectid(course), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- MODULE CRUD -----------------
class ModuleView(APIView):
    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        module_data = serializer.validated_data
        try:
            course_objid = ObjectId(module_data.get("course_id"))
        except InvalidId:
            return Response({"error": "Invalid course_id"}, status=status.HTTP_400_BAD_REQUEST)

        course = courses_collection.find_one({"_id": course_objid})
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        module_to_insert = {k: v for k, v in module_data.items() if k != "course_id"}
        module_to_insert.setdefault("topic_ids", [])
        result = modules_collection.insert_one(module_to_insert)
        courses_collection.update_one({"_id": course_objid}, {"$push": {"module_ids": result.inserted_id}})
        module_to_insert["_id"] = result.inserted_id
        return Response(convert_objectid(module_to_insert), status=status.HTTP_201_CREATED)

    def get(self, request):
        modules = list(modules_collection.find())
        for module in modules:
            topic_list = list(topics_collection.find({"_id": {"$in": module.get("topic_ids", [])}}))
            for topic in topic_list:
                content_list = list(contents_collection.find({"_id": {"$in": topic.get("content_ids", [])}}))
                topic["contents"] = content_list
            module["topics"] = topic_list
        return Response(convert_objectid(modules), status=status.HTTP_200_OK)

# ----------------- TOPIC CRUD -----------------
class TopicView(APIView):
    def get(self, request):
        topics = list(topics_collection.find())
        return Response(convert_objectid(topics), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TopicSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        topic_data = serializer.validated_data
        try:
            module_objid = ObjectId(topic_data.get("module_id"))
        except InvalidId:
            return Response({"error": "Invalid module_id"}, status=status.HTTP_400_BAD_REQUEST)

        module = modules_collection.find_one({"_id": module_objid})
        if not module:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

        topic_to_insert = {k: v for k, v in topic_data.items() if k != "module_id"}
        result = topics_collection.insert_one(topic_to_insert)
        modules_collection.update_one({"_id": module_objid}, {"$push": {"topic_ids": result.inserted_id}})
        topic_to_insert["_id"] = result.inserted_id
        return Response(convert_objectid(topic_to_insert), status=status.HTTP_201_CREATED)

class TopicDetailView(APIView):
    def get(self, request, topic_id):
        try:
            topic_objid = ObjectId(topic_id)
        except InvalidId:
            return Response({"error": "Invalid topic_id"}, status=status.HTTP_400_BAD_REQUEST)

        topic = topics_collection.find_one({"_id": topic_objid})
        if not topic:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(convert_objectid(topic), status=status.HTTP_200_OK)

    def put(self, request, topic_id):
        serializer = TopicSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = topics_collection.update_one({"_id": ObjectId(topic_id)}, {"$set": serializer.validated_data})
        if result.matched_count == 0:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        topic = topics_collection.find_one({"_id": ObjectId(topic_id)})
        return Response(convert_objectid(topic), status=status.HTTP_200_OK)

    def delete(self, request, topic_id):
        topic_objid = ObjectId(topic_id)
        result = topics_collection.delete_one({"_id": topic_objid})
        if result.deleted_count == 0:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
        modules_collection.update_many({}, {"$pull": {"topic_ids": topic_objid}})
        return Response({"message": "Topic deleted successfully"}, status=status.HTTP_200_OK)

# ----------------- CONTENT CRUD -----------------
class ContentView(APIView):
    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        content_data = serializer.validated_data
        try:
            topic_objid = ObjectId(content_data.get("topic_id"))
        except InvalidId:
            return Response({"error": "Invalid topic_id"}, status=status.HTTP_400_BAD_REQUEST)

        topic = topics_collection.find_one({"_id": topic_objid})
        if not topic:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

        content_to_insert = {"version": content_data["version"]}
        result = contents_collection.insert_one(content_to_insert)
        topics_collection.update_one({"_id": topic_objid}, {"$push": {"content_ids": result.inserted_id}})
        content_to_insert["_id"] = result.inserted_id
        return Response(convert_objectid(content_to_insert), status=status.HTTP_201_CREATED)

# ----------------- USER PROGRESS -----------------
class UpdateUserProgressView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get("user_id")
        course_id = data.get("course_id")
        module_id = data.get("module_id")
        topic_id = data.get("topic_id")
        content_id = data.get("content_id")

        if not all([user_id, course_id, module_id, topic_id, content_id]):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = update_user_progress(user_id, course_id, module_id, topic_id, content_id)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ----------------- ENROLLMENT CRUD -----------------
class EnrollmentCreateView(APIView):
    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            result = enrollments_collection.insert_one(serializer.validated_data)
            data = serializer.validated_data
            data["_id"] = result.inserted_id
            return Response(convert_objectid(data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentListView(APIView):
    def get(self, request):
        enrollments = list(enrollments_collection.find())
        return Response(convert_objectid(enrollments), status=status.HTTP_200_OK)

class EnrollmentUpdateView(APIView):
    def put(self, request, enrollment_id):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            result = enrollments_collection.update_one({"_id": ObjectId(enrollment_id)}, {"$set": serializer.validated_data})
            if result.matched_count == 0:
                return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)
            data = serializer.validated_data
            data["_id"] = enrollment_id
            return Response(convert_objectid(data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentDeleteView(APIView):
    def delete(self, request, enrollment_id):
        result = enrollments_collection.delete_one({"_id": ObjectId(enrollment_id)})
        if result.deleted_count == 0:
            return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Enrollment deleted"}, status=status.HTTP_204_NO_CONTENT)
