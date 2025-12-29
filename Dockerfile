# Use the official Python image
FROM python:3.14-slim

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy the project files
COPY . .

# Sync dependencies using uv
RUN uv sync --frozen

# Expose the port (Cloud Run defaults to 8080)
ENV PORT 8080

# Run the application with Gunicorn
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
