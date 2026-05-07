FROM mambaorg/micromamba:1.5.10

WORKDIR /app

COPY environment.yml /app/environment.yml
RUN micromamba install -y -n base -f /app/environment.yml && micromamba clean -a -y

COPY . /app

WORKDIR /app/backend

EXPOSE 8000

CMD ["micromamba", "run", "-n", "base", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
