# 使用官方 Python 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 设置环境变量（如果需要）
# ENV ...

# 暴露端口（Flask 应用默认端口为 5000）
EXPOSE 5000

# 运行 Flask 应用
CMD ["python", "app.py"]