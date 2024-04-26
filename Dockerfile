FROM python:3.9-slim AS builder

# Set up shell and Python environment settings
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

# Install system dependencies required to build Python packages
# such as numpy, pandas, etc. and clean up the apt cache once
# the packages are installed
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
      gcc \
      python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# Create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3.9 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install project dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt


FROM python:3.9-slim AS runtime

COPY --from=builder /opt/venv /opt/venv

# Activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the project code and notebooks into the container
COPY ./absenteeism /app/absenteeism
COPY ./notebooks /app/notebooks
WORKDIR /app

# Copy entrypoint script into the container
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set up non-root user
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["run_notebook"]