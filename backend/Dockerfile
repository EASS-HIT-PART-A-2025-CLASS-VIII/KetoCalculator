# syntax=docker/dockerfile:1

FROM public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 AS lwa
FROM public.ecr.aws/lambda/python:3.12

# Adapter extension
COPY --from=lwa /lambda-adapter /opt/extensions/aws-lambda-adapter

WORKDIR ${LAMBDA_TASK_ROOT}

# Install dependencies (deterministic)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app ./app

ENV PORT=8080

# Handler target (web adapter will serve the HTTP)
CMD ["app.main:app"]
