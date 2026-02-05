from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import os
from datetime import datetime
from dotenv import load_dotenv
from bson import ObjectId

This_Api = "http://127.0.0.1:8000/get_blog/"
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

app = FastAPI()


client = pymongo.MongoClient(mongo_uri)
db = client["blog_platform"]
collection = db["posts"]


class BlogModel(BaseModel):
    user_name: str
    title: str
    description: str


@app.post("/create_blog")
async def create_blog(blog: BlogModel):
    current_time = datetime.now()

    new_blog = {
        "user_name": blog.user_name,
        "title": blog.title,
        "description": blog.description,
        "date": current_time.strftime("%Y-%m-%d"),
        "time": current_time.strftime("%H:%M:%S"),
        "created_at": current_time,
    }

    result = collection.insert_one(new_blog)

    return {
        "message": "Blog created successfully",
        "id": This_Api + str(result.inserted_id),
        "blog_title": new_blog["title"],
    }


@app.get("/get_blog/{blog_id}")
async def get_blog(blog_id: str):
    try:
        blog = collection.find_one({"_id": ObjectId(blog_id)})

        if blog:
            blog["_id"] = str(blog["_id"])
            return blog
        else:
            return {"error": "Blog not found"}

    except Exception as e:
        return {"error": "Invalid ID format"}


# --- 3. Delete Blog (New Route) ---
@app.delete("/delete_blog/{blog_id}")
async def delete_blog(blog_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(blog_id)})

        if result.deleted_count == 1:
            return {"message": "Blog and User data deleted successfully"}
        else:
            return {"error": "Blog not found with this ID"}

    except Exception:
        return {"error": "Invalid ID format"}


@app.get("/get_all_blogs")
async def get_all_blogs():
    blogs = []
    cursor = collection.find({}).sort("created_at", -1)

    for blog in cursor:
        blog["_id"] = str(blog["_id"])
        blogs.append(blog)

    return {"total": len(blogs), "data": blogs}
