# Stage 1: Base build stage
FROM python:3.10.17-slim AS builder

# Install required packages
USER root
RUN <<EOF
apt-get -qq update
apt-get -q -y upgrade
apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config
rm -rf /var/lib/apt/lists/*
EOF

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Stage 2: Production stage
FROM python:3.10.17-slim

RUN <<EOF
apt-get -qq update
apt-get -q -y upgrade
apt-get install -y libmariadb3
rm -rf /var/lib/apt/lists/*
EOF

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Override Django admin menu
COPY ./menu.html /usr/local/lib/python3.10/site-packages/django_admin_kubi/templates/admin/

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setup an app user so the container doesn't run as the root user
USER 1000

# Expose the application port
EXPOSE 6969 

# Make entry file executable
RUN chmod +x ./entrypoint.sh

# Start the application using Gunicorn
CMD ["/app/entrypoint.sh"]
