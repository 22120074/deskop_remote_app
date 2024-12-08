# Sử dụng base image Python
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file yêu cầu và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép đoạn mã Python vào container
COPY server.py .

# Chạy đoạn mã Python
CMD ["python", "server.py"]
