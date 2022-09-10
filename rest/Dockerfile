FROM python	

RUN apt-get update
RUN pip install flask
RUN pip install flask_restful
RUN pip install flask_cors
RUN pip install numpy-stl
RUN pip install pysqlite3

RUN mkdir /home/rest
RUN mkdir /home/rest/files

COPY rest.py /home/rest

EXPOSE 5000

WORKDIR /home/rest
ENTRYPOINT ["python"]
CMD ["rest.py"]