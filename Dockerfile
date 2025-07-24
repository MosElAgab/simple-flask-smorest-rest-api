FROM python:3.11.1

# Create a non-root user without a home directory
RUN adduser --disabled-password --no-create-home app

# Set working directory
WORKDIR /app

# Copy dependencies file and install with root
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt (prod no need for cache)
RUN pip install -r requirements.txt

# Copy rest of the app code and change ownership
COPY . .
RUN chown -R app:app /app

# Switch to non-root user AFTER setup is done
USER app

EXPOSE 5000

## run
# dev
# CMD ["flask", "run", "--host", "0.0.0.0"]
# prod
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "--timeout", "30", "app:create_app()"]
# workers to be adjusted based on the host machine spec