#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Code from https://github.com/jasonqng/genius-lyrics-search adapted to suit my needs
# All credit goes to Jason Q. Ng

import sys  
import re
import urllib2
import json
import csv
import codecs
import os
import socket
from socket import AF_INET, SOCK_DGRAM

def load_credentials():
    lines = [line.rstrip('\n') for line in open('credentials.ini')]
    chars_to_strip = " \'\""
    for line in lines:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        #Currently only need access token to run, the other two perhaps for future implementation
        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
    return client_id, client_secret, client_access_token

    
def search(search_term,client_access_token):
    
    # We search for the URL
    querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_term) + "&page=" + str(1)
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + client_access_token)   
    request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
    while True:
        try:
            response = urllib2.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
            raw = response.read()
        except socket.timeout:
            print("Timeout raised and caught")
            continue
        break
    json_obj = json.loads(raw)
    body = json_obj["response"]["hits"]

    num_hits = len(body)
    if num_hits==0:
        print("No results for: " + search_term)
        exit(0)

    for result in body:
        url = ""
        song_test = result["index"] == 'song'
        if song_test:
            title = result["result"]["title"]
            url = result["result"]["url"]
            path = result["result"]["path"]
            primaryartist_name = result["result"]["primary_artist"]["name"]
            break # We have faith in Genius search engine :-)
    return url


def main():
    arguments = sys.argv[1:] #so you can input searches from command line if you want
    search_term = arguments[0].translate(None, "\'\"")
    client_id, client_secret, client_access_token = load_credentials()
    search(search_term,client_access_token)

if __name__ == '__main__':
    main()
