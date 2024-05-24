FROM python:3.11-alpine
RUN apk add --no-cache nodejs npm
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN npm install --prefix src
RUN npm cache clean --force && rm -rf /var/cache/apk/*
EXPOSE 8000
EXPOSE 8050
CMD ["invoke", "devallall"]
