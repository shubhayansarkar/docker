# init a base image (Alpine is small Linux distro)
FROM python:3.7
# define the present working directory
WORKDIR /project1
# copy the contents into the working dir
ADD . /project1
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python","app.py"]