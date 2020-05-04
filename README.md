# Django Server Sent Event (SSE)

### Prerequisite:
* python3    
* redis

### Usage:
```bash
$ pip install -r requirements.txt
$ cd src
$ ./manage.py migrate
$ ./manage.py runserver                             (terminal 1)
$ celery -A youtube_downloader worker -l info -E    (terminal 2)
```