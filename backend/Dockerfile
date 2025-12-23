# syntax=docker/dockerfile:1

FROM public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 AS lwa
FROM public.ecr.aws/lambda/python:3.12

COPY --from=lwa /lambda-adapter /opt/extensions/aws-lambda-adapter
WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.runtime.txt ./
RUN sed -i \
      -e '/^file:\/\//d' \
      -e '/^-e[[:space:]]\+\./d' \
      -e '/^\.[[:space:]]*$/d' \
      requirements.runtime.txt \
    && pip install --no-cache-dir -r requirements.runtime.txt

COPY app ./app

ENV PORT=8080
CMD ["app.main:app"]
