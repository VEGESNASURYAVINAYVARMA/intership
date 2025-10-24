from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from bson import ObjectId
from .mongo import quiz_collection
from .serializers import QuizSerializer

# -------------------------
# CREATE QUIZ
# -------------------------
@api_view(['POST'])
def create_quiz(request):
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        now = datetime.utcnow()
        data['metadata']['created_at'] = now
        data['metadata']['updated_at'] = now

        # Ensure defaults
        data['status'] = data.get('status', 'active')
        data['points'] = data.get('points', 1)
        data['mode'] = data.get('mode', 'manual')

        quiz_collection.insert_one(data)
        return Response({"message": "Quiz created successfully"}, status=201)
    
    return Response(serializer.errors, status=400)

# -------------------------
# LIST ALL QUIZZES
# -------------------------
@api_view(['GET'])
def list_quizzes(request):
    quizzes = list(quiz_collection.find())
    for quiz in quizzes:
        quiz["_id"] = str(quiz["_id"])
    return Response(quizzes)

# -------------------------
# RETRIEVE FULL QUIZ BY ID
# -------------------------
@api_view(['GET'])
def retrieve_quiz(request, quiz_id):
    """
    Return full quiz document by quiz_id.
    Works with both string IDs and Mongo ObjectId.
    """
    quiz = quiz_collection.find_one({"_id": quiz_id})

    if not quiz and ObjectId.is_valid(quiz_id):
        quiz = quiz_collection.find_one({"_id": ObjectId(quiz_id)})

    if not quiz:
        return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    quiz["_id"] = str(quiz["_id"])
    return Response(quiz)

# -------------------------
# UPDATE QUIZ BY ID
# -------------------------
@api_view(['PUT'])
def update_quiz(request, quiz_id):
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        data['metadata']['updated_at'] = datetime.utcnow()

        filter_id = quiz_id if quiz_collection.find_one({"_id": quiz_id}) else \
                    ObjectId(quiz_id) if ObjectId.is_valid(quiz_id) else None
        if not filter_id:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        result = quiz_collection.update_one({"_id": filter_id}, {"$set": data})
        if result.matched_count:
            return Response({"message": "Quiz updated"})
        return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# DELETE QUIZ BY ID
# -------------------------
@api_view(['DELETE'])
def delete_quiz(request, quiz_id):
    filter_id = quiz_id if quiz_collection.find_one({"_id": quiz_id}) else \
                ObjectId(quiz_id) if ObjectId.is_valid(quiz_id) else None
    if not filter_id:
        return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    result = quiz_collection.delete_one({"_id": filter_id})
    if result.deleted_count:
        return Response({"message": "Quiz deleted"})
    return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
