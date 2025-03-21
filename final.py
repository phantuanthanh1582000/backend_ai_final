import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from io import BytesIO
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from PIL import Image

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Load biến môi trường
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not HUGGINGFACE_API_KEY:
    raise Exception("🚨 Chưa thiết lập HUGGINGFACE_API_KEY trong file .env")
if not MONGO_URI:
    raise Exception("🚨 Chưa thiết lập MONGO_URI trong file .env")
if not DB_NAME:
    raise Exception("🚨 Chưa thiết lập DB_NAME trong file .env")

# Kết nối MongoDB
try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    products_collection = db["products"]
    print("✅ Kết nối MongoDB thành công!")
except Exception as e:
    raise Exception(f"❌ Lỗi kết nối MongoDB: {str(e)}")

# Khởi tạo FastAPI
app = FastAPI(title="E-commerce AI Integrated API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load mô hình MobileNet của TensorFlow
model = MobileNet(weights='imagenet')

@app.post("/classify_image")
async def classify_image(file: UploadFile = File(...)):
    """ Phân loại ảnh sản phẩm bằng MobileNet """
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents)).convert("RGB")
        img = img.resize((224, 224))

        # Tiền xử lý ảnh
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Dự đoán ảnh
        preds = model.predict(x)
        predictions = decode_predictions(preds, top=3)[0]

        # Định dạng kết quả
        results = [{"label": label, "description": desc, "confidence": float(conf)} for (label, desc, conf) in predictions]
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý ảnh: {str(e)}")

@app.post("/analyze_review")
async def analyze_review(request: dict):
    """ Phân tích cảm xúc từ đánh giá khách hàng sử dụng Hugging Face API """
    review = request.get("review")  
    if not review:
        raise HTTPException(status_code=400, detail="Thiếu nội dung review")

    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": review}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Lỗi API Hugging Face: {response.text}")

    result = response.json()
    return {"analysis": result}

class RecommendationRequest(BaseModel):
    search_query: str  # Từ khóa tìm kiếm sản phẩm

@app.post("/recommend_products")
async def recommend_products(request: RecommendationRequest):
    """ Tìm sản phẩm phù hợp trong MongoDB theo từ khóa tìm kiếm """
    try:
        query = request.search_query.strip().lower()
        if not query:
            raise HTTPException(status_code=400, detail="Từ khóa tìm kiếm không hợp lệ.")

        # Tìm sản phẩm chứa từ khóa (không phân biệt chữ hoa/thường)
        products_cursor = products_collection.find(
            {"name": {"$regex": query, "$options": "i"}},
            {"_id": 0, "name": 1, "category": 1, "price": 1, "image_url": 1}
        )

        # Chuyển cursor thành danh sách
        products = await products_cursor.to_list(length=10)  # Giới hạn 10 sản phẩm

        if not products:
            return {"message": "Không tìm thấy sản phẩm phù hợp", "recommendations": []}

        return {"recommendations": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi truy vấn dữ liệu: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
