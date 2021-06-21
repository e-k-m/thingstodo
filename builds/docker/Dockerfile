FROM python:3.8-slim

ARG extra_index_url

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY ./README.md /app/README.md
COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py
COPY thingstodo /app/thingstodo
RUN pip install --upgrade pip && \
    pip install  --extra-index-url=$extra_index_url -e . && \
    pip install gunicorn[gevent]==20.0.4

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "--worker-class", "gevent", "thingstodo:app"]