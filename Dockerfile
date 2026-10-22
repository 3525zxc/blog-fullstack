# suga.app 等容器平台构建镜像使用
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# 先装依赖（利用 Docker 层缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制全部代码（server/ + web/）
COPY . .

EXPOSE 8000

# 必须绑定 0.0.0.0，端口取平台注入的 PORT（默认 8000）
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 server.app:app"]
