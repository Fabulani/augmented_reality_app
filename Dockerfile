FROM python:3.8

# Should fix access rights for webcam on Unix
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    adduser appuser video
USER appuser

# Install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt