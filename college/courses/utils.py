# from bson import ObjectId
# from datetime import datetime
# from .mongo_utils import get_db_handle

# db = get_db_handle()
# user_progress_collection = db["user_progress"]


# def update_user_progress(user_id, course_id, module_id, topic_id, content_id):
#     """
#     Updates user's progress from content → topic → module → course.
#     Called whenever a content is completed.
#     """

#     user_progress = user_progress_collection.find_one({"user_id": user_id})
#     if not user_progress:
#         raise ValueError("User progress record not found")

#     # Find the specific course in user's progress
#     for course in user_progress.get("courses", []):
#         if str(course["course_id"]) == str(course_id):

#             # Go to module
#             for module in course.get("modules", []):
#                 if str(module["module_id"]) == str(module_id):

#                     # Go to topic
#                     for topic in module.get("topics", []):
#                         if str(topic["topic_id"]) == str(topic_id):

#                             # Find content and mark it complete
#                             for content in topic.get("contents", []):
#                                 if str(content["content_id"]) == str(content_id):
#                                     content["completed"] = True
#                                     content["progress_percentage"] = 100
#                                     content["completion_date"] = datetime.utcnow().isoformat()

#                             # Recalculate topic progress
#                             total_contents = len(topic["contents"])
#                             completed_contents = sum(1 for c in topic["contents"] if c["completed"])
#                             topic_percentage = (completed_contents / total_contents) * 100 if total_contents else 0
#                             topic["topic_percentage"] = topic_percentage
#                             topic["completed"] = topic_percentage == 100

#                     # Recalculate module progress
#                     total_topics = len(module["topics"])
#                     total_topic_progress = sum(t["topic_percentage"] for t in module["topics"])
#                     module_progress = total_topic_progress / total_topics if total_topics else 0
#                     module["progress_percentage"] = module_progress
#                     module["completed"] = module_progress == 100

#             #  Recalculate course progress
#             total_modules = len(course["modules"])
#             total_module_progress = sum(m["progress_percentage"] for m in course["modules"])
#             course_progress = total_module_progress / total_modules if total_modules else 0
#             course["course_progress_percentage"] = course_progress
#             course["completed"] = course_progress == 100

#             # Update last_updated
#             course["last_updated"] = datetime.utcnow().isoformat()

#     # Save updated document
#     user_progress_collection.update_one(
#         {"user_id": user_id},
#         {"$set": user_progress}
#     )

#     return {"message": "Progress updated successfully"}
from bson import ObjectId
from datetime import datetime
from .mongo_utils import get_db_handle

db = get_db_handle()
user_progress_collection = db["user_progress"]

def update_user_progress(user_id, course_id, module_id, topic_id, content_id):
    """
    Updates user's progress from content → topic → module → course.
    Called whenever a content is completed.
    """

    user_progress = user_progress_collection.find_one({"user_id": user_id})
    if not user_progress:
        raise ValueError("User progress record not found")

    for course in user_progress.get("courses", []):
        if str(course["course_id"]) == str(course_id):
            for module in course.get("modules", []):
                if str(module["module_id"]) == str(module_id):
                    for topic in module.get("topics", []):
                        if str(topic["topic_id"]) == str(topic_id):
                            for content in topic.get("contents", []):
                                if str(content["content_id"]) == str(content_id):
                                    content["completed"] = True
                                    content["progress_percentage"] = 100
                                    content["completion_date"] = datetime.utcnow().isoformat()
                            # Topic progress
                            total_contents = len(topic["contents"])
                            completed_contents = sum(1 for c in topic["contents"] if c["completed"])
                            topic_percentage = (completed_contents / total_contents) * 100 if total_contents else 0
                            topic["topic_percentage"] = topic_percentage
                            topic["completed"] = topic_percentage == 100
                    # Module progress
                    total_topics = len(module["topics"])
                    module_progress = sum(t["topic_percentage"] for t in module["topics"]) / total_topics if total_topics else 0
                    module["progress_percentage"] = module_progress
                    module["completed"] = module_progress == 100
            # Course progress
            total_modules = len(course["modules"])
            course_progress = sum(m["progress_percentage"] for m in course["modules"]) / total_modules if total_modules else 0
            course["course_progress_percentage"] = course_progress
            course["completed"] = course_progress == 100
            course["last_updated"] = datetime.utcnow().isoformat()

    user_progress_collection.update_one({"user_id": user_id}, {"$set": user_progress})
    return {"message": "Progress updated successfully"}
