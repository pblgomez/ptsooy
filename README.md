# ptsooy
Podcast the s\*\*\* out of youtube

A little program that takes your youtube subscriptions and downloads all the Videos and creates xml files for your favourite podcast player

1. Download the subscription_manager.opml from youtube

1. Rename and modify variables.example.py to variables.py

1. Run:
  ```
  ptsooy.py -i /path/to/subscription_manager.opml
  ```
  or just place the subscription_manager.opml file in the same directory


## For docker (wip)
docker run -d --name ptsooy -p 8080:8080 -v path/to/Videos/:/Videos local/ptsooy
