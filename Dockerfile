FROM python:2-onbuild
CMD [ "python", "./rss-filter.py", "runserver", "-h", "0.0.0.0", "-p", "5000" ]
EXPOSE 5000
