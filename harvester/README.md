Tweet Crawler
-------------

## Instructions

Linux:

```sh
# set up a virtualenv
python3 -m venv venv
source ./venv/bin/activate
# install dependencies
pip3 install -r requirements.txt
# run
python tweet_crawler.py
```
## Background forking

```
chmod +x tweet_crawler.py
./tweet_crawler.py 2>&1 > /dev/null &

pgrep -l python
```
