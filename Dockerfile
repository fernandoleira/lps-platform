FROM python:3.9.1-slim
# Image Labels
LABEL org.opencontainers.image.authors="LeiraFernandoCortel@gmail.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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
CMD ["-w", "1", "--bind", "0.0.0.0:5000", "lps:app"]