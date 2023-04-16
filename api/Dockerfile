FROM python:3.10.4-slim AS base

# Set python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    VENV_PATH="/opt/venv"

# Add venv to Path
ENV PATH="${VENV_PATH}/bin:${PATH}"

# Update and upgrade the image
RUN apt update && apt upgrade -y

# Set pip envs
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Install hatch (used later, not needed in venv)
RUN pip install hatch

# Create virtual environment
RUN python -m venv ${VENV_PATH}

WORKDIR /app/api

# Install depdendencies
COPY pyproject.toml .
RUN hatch dep show requirements | xargs pip install  

# TODO: remove
RUN pip install ipdb

# Install api
COPY src logo.png ai-plugin.json .
RUN pip install --no-deps . 

FROM base as api

COPY --from=base ${VENV_PATH} ${VENV_PATH}

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
