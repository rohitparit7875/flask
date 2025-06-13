# select the base image which has got python installed
FROM python

# set the working directory
WORKDIR /src

# copy everything from current working directory to image working directory
COPY . .

# export port 3000
EXPOSE 4000

# install flask while building the image
RUN pip install flask

# run the server
CMD python3 server.py

