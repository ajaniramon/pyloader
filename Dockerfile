#
FROM python:3.8 as base
EXPOSE 8000
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home pyloader
WORKDIR /home/pyloader
USER pyloader

# Install application into container
COPY . .

ENV ADMIN_USER=admin
ENV ADMIN_PASSWORD=admin

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
