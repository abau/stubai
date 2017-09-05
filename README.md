# stubai

Plot GPX tracks using MapQuest's OpenStreetMap API:

```
./stubai.py --width=500 --height=500 --output=example.jpg ${API_KEY} track.gpx
```

![map.jpg](https://raw.githubusercontent.com/abau/stubai/master/example.jpg)

Get your API key at https://developer.mapquest.com.

## Help

```
$ ./stubai.py --help
usage: stubai.py [-h] [--output FILE] [--width WIDTH] [--height HEIGHT]
                 [--zoom N] [--skip-lead N] [--skip-trail N]
                 [--include-every N] [--waypoints FILE] [--start-waypoint]
                 [--end-waypoint] [--print-url]
                 KEY FILE

Plot GPX tracks using MapQuest's OpenStreetMap API

positional arguments:
  KEY                MapQuest API key
  FILE               GPX file

optional arguments:
  -h, --help         show this help message and exit
  --output FILE      Output file
  --width WIDTH      Width of the resulting image
  --height HEIGHT    Height of the resulting image
  --zoom N           Zoom level
  --skip-lead N      Skip N leading track points
  --skip-trail N     Skip N trailing track points
  --include-every N  Include every N-th trailing track point only
  --waypoints FILE   GPX file containing waypoints
  --start-waypoint   Add start waypoint
  --end-waypoint     Add end waypoint
  --print-url        Print requested URL
```
