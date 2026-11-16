FROM squidfunk/mkdocs-material:latest
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt