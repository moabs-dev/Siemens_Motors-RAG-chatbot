# # FROM python:3.11-slim

# # WORKDIR /app

# # # Copy shared requirements
# # COPY requirements.txt .

# # RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt


# # # Copy frontend code
# # COPY Frontend/ ./Frontend

# # # Run Streamlit app
# # CMD ["streamlit", "run", "frontend2.py", "--server.port=8501", "--server.address=0.0.0.0"]

# FROM python:3.11-slim

# WORKDIR /app

# # Copy requirements
# COPY ../requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Copy frontend code
# COPY . .

# # Expose Streamlit port
# EXPOSE 8501

# # Start Streamlit
# CMD ["streamlit", "run", "frontend2.py", "--server.port=8501", "--server.address=0.0.0.0"]

FROM python:3.11-slim

WORKDIR /app

# Copy requirements from root (now allowed)
COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy frontend code
COPY . .

#EXPOSE 8501

CMD ["streamlit", "run", "frontend2.py", "--server.port=8501", "--server.address=0.0.0.0"]
