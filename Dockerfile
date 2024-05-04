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
#Running your APP and doing some PORT Forwarding
CMD ["python","./app/app.py"]