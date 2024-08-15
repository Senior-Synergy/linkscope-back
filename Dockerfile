# Base image
FROM public.ecr.aws/lambda/python:3.11

# Install system-level dependencies
RUN yum -y update && \
    yum -y groupinstall "Development Tools" && \
    yum clean all

COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY data/model.joblib ${LAMBDA_TASK_ROOT}/data/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY app/ ${LAMBDA_TASK_ROOT}/app/

CMD [ "app.main.handler" ]

# Notes from P.W.:
# By the way, LAMBDA_TASK_ROOT is an env. variable that is available
# to the dockerfile when it is building, and this is where :ambda
# will consider the root path of our function...