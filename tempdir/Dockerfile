FROM python
COPY ./requirements.txt /home/myapp/
RUN pip install -r /home/myapp/requirements.txt
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  design.py /home/myapp/
EXPOSE 5050
CMD python /home/myapp/design.py
