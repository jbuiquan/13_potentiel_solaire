FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install poetry==1.8.5
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies and the local package
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

# Copy algorithme files
COPY alembic.ini ./
COPY database ./database
COPY potentiel_solaire ./potentiel_solaire
COPY notebooks/pipeline_algorithme.ipynb ./notebooks/pipeline_algorithme.ipynb
COPY README.md ./

ENTRYPOINT ["poetry", "run"]  
