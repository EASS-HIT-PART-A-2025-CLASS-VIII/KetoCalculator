FROM public.ecr.aws/docker/library/python:3.12-slim

# Lambda Web Adapter extension
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 \
  /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /var/task

# 1) Install deps (NO uv at runtime)
COPY requirements.runtime.txt ./
RUN pip install --no-cache-dir -r requirements.runtime.txt

# 2) Copy app
COPY app ./app

# Web adapter default is 8080 (keep it simple) :contentReference[oaicite:2]{index=2}
ENV PORT=8080
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
