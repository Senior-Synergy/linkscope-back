FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY config.json ${LAMBDA_TASK_ROOT}
COPY data/model_compressed.gzip ${LAMBDA_TASK_ROOT}/data/

RUN pip install -r requirements.txt

COPY app/ ${LAMBDA_TASK_ROOT}/app/

CMD [ "app.main.handler" ]

# Notes from P.W.:
# By the way, LAMBDA_TASK_ROOT is an env. variable that is available
# to the dockerfile when it is building, and this is where :ambda
# will consider the root path of our function...