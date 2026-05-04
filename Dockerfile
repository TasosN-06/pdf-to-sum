FROM python:3.10-slim

# Δημιούργησε non-root user (απαίτηση HF Spaces)
RUN useradd -m -u 1000 user

# Set environment για τον user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /home/user/app

# Εγκατάσταση dependencies ως user
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy κώδικα με σωστά permissions
COPY --chown=user main.py .
COPY --chown=user app/ ./app/
COPY --chown=user static/ ./static/

USER user

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]