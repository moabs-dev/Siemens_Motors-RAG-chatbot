# # FROM python:3.11-slim

# # WORKDIR /app

# # # Copy shared requirements
# # COPY requirements.txt .

# # RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt


# # # Copy backend code
# # COPY Backend/ ./Backend

# # # Run FastAPI with uvicorn
# # CMD ["uvicorn", "backend2:app", "--host", "0.0.0.0", "--port", "8000"]

# FROM python:3.11-slim

# WORKDIR /app

# # Copy requirements
# COPY ../requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Copy backend code
# COPY . .

# # Expose FastAPI port
# EXPOSE 8000

# # Start FastAPI with Uvicorn
# CMD ["uvicorn", "backend2:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

WORKDIR /app

# # Copy requirements from root
# COPY requirements.txt .
COPY . ./Backend

#RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt
COPY requirements.base.txt .
RUN pip install --no-cache-dir -r requirements.base.txt

COPY requirements.heavy.txt .
RUN pip install --no-cache-dir -r requirements.heavy.txt

# Copy backend code
COPY . .


#EXPOSE 8000

CMD ["uvicorn", "Backend.backend2:app", "--host", "0.0.0.0", "--port", "8000"]
