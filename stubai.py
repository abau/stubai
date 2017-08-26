#!/bin/python3

import xml.sax
import requests
import argparse
import os.path
import sys

parser = argparse.ArgumentParser (description = "Make MapQuest maps from GPX files")
parser.add_argument ("--output", metavar = "FILE", type = str, default = "", help = "Output file")
parser.add_argument ("--width", metavar = "WIDTH", type = int, default = 1920, help = "Width of the resulting image")
parser.add_argument ("--height", metavar = "HEIGHT", type = int, default = 1920, help = "Height of the resulting image")
parser.add_argument ("--zoom", metavar = "N", type = int, default = None, help = "Zoom level")
parser.add_argument ("--skip-lead", metavar = "N", type = int, default = 0, help = "Skip N leading track points")
parser.add_argument ("--skip-trail", metavar = "N", type = int, default = 0, help = "Skip N trailing track points")
parser.add_argument ("--include-every", metavar = "N", type = int, default = 1, help = "Include every N-th trailing track point only")
parser.add_argument ("--print-url", action = "store_true", help = "Print requested URL")
parser.add_argument ("key", metavar = "KEY", help = "MapQuest API key")
parser.add_argument ("file", metavar = "FILE", help = "GPX file")

class LatLonHandler (xml.sax.ContentHandler):
    def __init__ (self):
        self.encodedLocations = []
        self.numLocations = 0
        self.latestLat = 0
        self.latestLon = 0

    def encode (n):
        n = n << 1
        if n < 0:
            n = ~n
        encN = ""
        while n >= 0x20:
            encN += chr ((0x20 | (n & 0x1F)) + 63)
            n = n >> 5

        return encN + chr (n + 63)

    def addEncodedLatLon (self, lat, lon):
        rLat = int (round (lat * pow (10, 5)))
        rLon = int (round (lon * pow (10, 5)))

        encLat = LatLonHandler.encode (rLat - self.latestLat)
        encLon = LatLonHandler.encode (rLon - self.latestLon)

        self.encodedLocations.append (encLat + encLon)

        self.latestLat = rLat
        self.latestLon = rLon

    def startElement (self, name, attrs):
        if name == "trkpt":
            afterSkip = self.numLocations >= args.skip_lead
            include = afterSkip and ((self.numLocations - args.skip_lead) % args.include_every == 0)

            if (include):
                lat = float (attrs.getValue ("lat"))
                lon = float (attrs.getValue ("lon"))

                self.addEncodedLatLon (lat, lon)

            self.numLocations += 1
    
if __name__ == "__main__":
    args = parser.parse_args ()
    parser = LatLonHandler ()
    xml.sax.parse (args.file, parser)

    if args.skip_trail > 0:
        parser.encodedLocations = parser.encodedLocations[0:-args.skip_trail]

    locations = "".join (parser.encodedLocations)
    url = ("https://www.mapquestapi.com/staticmap/v5/map"
           "?size={},{}"
           "&key={}"
           "&shape=cmp|enc:{}"
          ).format (args.width, args.height, args.key, locations)

    if args.zoom:
        url += "&zoom={}".format (args.zoom)

    if args.print_url:
        print (url)

    req = requests.get (url)

    if req.status_code == 200:
        output = os.path.basename (args.file) + ".jpg"
        if args.output:
            output = args.output

        with open (output, "wb") as file:
            file.write (req.content)

        sys.exit ()
    else:
        sys.exit (__file__ + ": " + req.text)
