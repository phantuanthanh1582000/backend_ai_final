# 🚀 E-commerce AI - Backend

## 📌 Giới thiệu

Backend của E-commerce AI cung cấp các API để hỗ trợ:

- **Phân loại ảnh**: Nhận diện sản phẩm từ hình ảnh tải lên bằng TensorFlow.
- **Phân tích nhận xét**: Đánh giá cảm xúc của khách hàng bằng Hugging Face API.
- **Gợi ý sản phẩm**: Tìm sản phẩm phù hợp dựa trên từ khóa tìm kiếm trong MongoDB.

Backend được xây dựng bằng **FastAPI**, sử dụng **TensorFlow**, **Hugging Face API**, và **MongoDB**.

---

## 🛠️ Công nghệ sử dụng

- **Framework**: FastAPI
- **Trí tuệ nhân tạo**: TensorFlow, Hugging Face API
- **Cơ sở dữ liệu**: MongoDB
- **Deploy**: Render

---

## 🚀 Cài đặt và chạy backend

### 1️⃣ Yêu cầu

- Python >= 3.8
- MongoDB (Atlas hoặc cục bộ)

### 2️⃣ Clone repository

```sh
git clone https://github.com/phantuanthanh1582000/backend_ai_final.git
```

### 3️⃣ Tạo môi trường ảo và cài đặt dependencies

```sh
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate  # Trên Windows
pip install -r requirements.txt
```

### 4️⃣ Thiết lập biến môi trường

Tạo file `.env` và thêm các giá trị sau:

```
HUGGINGFACE_API_KEY=your_huggingface_api_key
MONGO_URI=your_mongodb_connection_string
DB_NAME=your_database_name
```

### 5️⃣ Chạy backend

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Sau khi chạy, API sẽ hoạt động tại: `http://localhost:8000`

---

## 📌 Hướng dẫn sử dụng API

### 🌍 Base URL

- **Local**: `http://localhost:8000`
- **Deploy**: `https://backend-ai-final.onrender.com`

### 📌 Endpoints

#### 1️⃣ **Phân loại ảnh**

- **Endpoint**: `POST /classify_image`
- **Mô tả**: Nhận diện sản phẩm từ ảnh tải lên.
- **Body**: `multipart/form-data`
  ```sh
  curl -X POST "https://backend-ai-final.onrender.com/classify_image" -F "file=@image.jpg"
  ```

#### 2️⃣ **Phân tích nhận xét**

- **Endpoint**: `POST /analyze_review`
- **Mô tả**: Phân tích cảm xúc từ nhận xét của khách hàng.
- **Body**: `{ "review": "so good" }`
  ```sh
  curl -X POST "https://backend-ai-final.onrender.com/analyze_review" -H "Content-Type: application/json" -d '{"review": "Sản phẩm rất tốt!"}'
  ```

#### 3️⃣ **Gợi ý sản phẩm**

- **Endpoint**: `POST /recommend_products`
- **Mô tả**: Tìm sản phẩm trong MongoDB theo từ khóa.
- **Body**: `{ "search_query": "giày thể thao" }`
  ```sh
  curl -X POST "https://backend-ai-final.onrender.com/recommend_products" -H "Content-Type: application/json" -d '{"search_query": "iphone"}'
  ```

---

## 🌍 Deploy

- **Backend**: [https://backend-ai-final.onrender.com](https://backend-ai-final.onrender.com)

---

## 📜 License

MIT License.

---

## ✨ Tác giả

**Phan Tuan Thanh**  
📧 Email: tphan10932@gmail.com  
🔗 GitHub: [phantuanthanh1582000](https://github.com/phantuanthanh1582000)
