#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp design.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.
cp requirements.txt tempdir/.

echo "FROM python" > tempdir/Dockerfile
echo "COPY ./requirements.txt /home/myapp/" >> tempdir/Dockerfile
echo "RUN pip install -r /home/myapp/requirements.txt" >> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  design.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 5050" >> tempdir/Dockerfile
echo "CMD python /home/myapp/design.py" >> tempdir/Dockerfile

cd tempdir
docker build -t designapp .
docker run -t -d -p 5050:5050 --name designrunning designapp
docker ps -a 
