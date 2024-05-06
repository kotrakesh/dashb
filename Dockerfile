#Using python
FROM python:3.11
# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app
#

ENV dash_port=80
ENV dash_debug="False"
CMD ["python","./app/app.py"]