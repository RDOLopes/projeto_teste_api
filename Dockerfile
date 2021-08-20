FROM python
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
WORKDIR /app
COPY app/requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./app /app

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV APP_PORT 5000
ENV APP_BIND_ADDR 0.0.0.0
ENV APP_DIR "/app"
ENV APP_MODULE_NAME "main"
ENV APP_NAME "app"