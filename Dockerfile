FROM python:3.9-slim

# Install dependencies and Rust (Cargo)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH=$HOME/.cargo/bin:$PATH && \
    rustup update

# Explicitly set the PATH in the same RUN command to ensure it's available for subsequent commands
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy requests python-dotenv passlib bcrypt "python-jose[cryptography]" python-multipart

# Expose the application port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
