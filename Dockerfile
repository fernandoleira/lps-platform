FROM python:3.9.1-slim
# Image Labels
LABEL org.opencontainers.image.authors="LeiraFernandoCortel@gmail.com"

# Copy files
COPY . .

# Install dependencies with pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 5000

# Set entrypoint as "flask"
ENTRYPOINT [ "flask" ]

# Command to run the app
CMD ["run", "--host", "0.0.0.0"]