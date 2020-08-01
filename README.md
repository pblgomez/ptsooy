# ptsooy
## Podcast the s*** out of youtube

A little program that takes your youtube subscriptions and downloads all the Videos and creates xml files for your favourite podcast player

## How to run

Download the subscription_manager from [here](https://www.youtube.com/subscription_manager)

### With Python poetry
```
poetry install
poetry run python src/ptsooy
```

## With docker
```
docker run --rm --name ptsooy pablogomez/ptsooy -p 80:80 -v path/to/Videos/:/Videos local/ptsooy
```

1. docker run -d --name ptsooy -p 8080:8080 -v path/to/Videos/:/Videos local/ptsooy


### docker
```
docker run --rm \
  -v /path/to/subscription_manager:/app/subscription_manager \
  -v /path/to/Videos/:/app/Videos/ \
  pablogomez/ptsooy \
  -i subscription_manager
  --date_after=20200731 \
  --vids_count=3 \
  --host=https://ptsooy.example.com \
  --port=80
```

### docker-compose
```
---
version: '3.6'
services:
  ptsooy:
    image: pablogomez/ptsooy
    container_name: ptsooy
    environment:
      - date_after: 20200731
      - vids_count: 3
      - host: https://ptsooy.example.com
      - port: 6969
    volumes:
      - /path/to/subscription_manager:/app/subscription_manager
      - /path/to/Videos/:/app/Videos/
    ports:
      - 8069:80
    restart: unless-stopped
```