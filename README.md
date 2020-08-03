# ptsooy
## Podcast the s*** out of youtube

A little program that takes your youtube subscriptions and downloads all the Videos and creates xml files for your favourite podcast player


## How to run

Download the subscription_manager from [here](https://www.youtube.com/subscription_manager)
Only use it when you want to import all subscriptions again. So you can delete this file and manage it with channels.yaml
### With Python poetry
```
poetry install
poetry run python src/ptsooy -i subscription_manager
```

## With docker
```
docker run --rm --name ptsooy \
  -p 80:80 \
  -v path/to/Videos/:/Videos pablogomez/ptsooy \
  -v $HOME/configs/ptsooy/subscription_manager:/app/subscription_manager \
  -e date_after=20200731 \
  -e vids_count=3
  -e host=https://ptsooy.example.com
  -e port=6969
  pablogomez/ptsooy
```


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