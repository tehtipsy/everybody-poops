FROM public.ecr.aws/docker/library/python:3.14-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && git clone https://github.com/tehtipsy/everybody-poops.git . \
    && useradd -m appuser && chown -R appuser /src

USER appuser

EXPOSE 8000

CMD ["python", "main.py"]