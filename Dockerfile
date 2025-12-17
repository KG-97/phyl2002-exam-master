FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY phyl2002_exam ./phyl2002_exam
COPY README.md .

ENTRYPOINT ["python", "-m", "phyl2002_exam.cli"]
CMD ["--help"]
