FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["/bin/bash", "-c", "streamlit run report.py --server.port=8501 --server.address=0.0.0.0 & python /app/main.py & wait"]

# CMD ["/usr/local/bin/python /app/main.py", "-f"]
