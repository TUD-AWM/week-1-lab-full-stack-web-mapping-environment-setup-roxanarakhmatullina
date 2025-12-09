# Use Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for GDAL and GeoDjango
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    binutils \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY ../../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY ../../ /app/

# Set environment variable for GDAL
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV PROJ_LIB=/usr/share/proj

# Expose the app port
EXPOSE 8000

# Collect static files, run migrations, and start Gunicorn
CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn activefinder.wsgi:application --bind 0.0.0.0:8000"]
