# Sử dụng image Python 3.9 slim
FROM python:3.9-slim

# Đặt biến môi trường để in log không bị buffering
ENV PYTHONUNBUFFERED=1

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt và cài đặt các thư viện
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Vô hiệu hóa GPU cho TensorFlow
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV CUDA_VISIBLE_DEVICES=-1
ENV TF_CPP_MIN_LOG_LEVEL=2

# Mở cổng 8000 để truy cập API
EXPOSE 8000

# Lệnh khởi động ứng dụng sử dụng uvicorn
CMD ["uvicorn", "final:app", "--host", "0.0.0.0", "--port", "8000"]
