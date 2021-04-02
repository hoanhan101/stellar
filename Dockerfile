FROM python:3.8

COPY . .

RUN pip install --disable-pip-version-check poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV PYTHONUNBUFFERED=1

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
