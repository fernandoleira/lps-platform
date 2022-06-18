FROM python:3.9.1-slim

# Image Labels
LABEL org.opencontainers.image.authors="LeiraFernandoCortel@gmail.com"
LABEL org.opencontainers.image.url="https://fernandoleira.me"
LABEL org.opencontainers.image.source="https://github.com/fernandoleira/lps-platform"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="Locator Pointer System (LPS)"
LABEL org.opencontainers.image.description="This is the docker image for the LPS platform server backend api"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV "production"

# Create /app folder
RUN mkdir /app
WORKDIR /app

# Copy files
COPY . .

# Install dependencies with pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 5000/tcp

# Set entrypoint as "gunicorn"
ENTRYPOINT ["gunicorn"]

# Command to run the app
CMD ["-w", "3", "--bind", "0.0.0.0:5000", "api:create_app()"]