FROM python:3.8


# Install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt