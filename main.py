#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
import re
import sys
import subprocess
from time import time

# pret is a transformer for the course code, before it's inserted into
# the url.

def get_url(course_code):
    """ Returns the url of the course code """
    # inst = institutions[course_code[1]]
    # d = urls[inst]
    # pret = d.get("pret") or (lambda x: x)
    # return (d["url"]).format(pret(course_code))
    return f"https://liu.se/studieinfo/kurs/{course_code}/"

def get_soup(url):
    """ Returns a BeatifulSoup object containing the response from url """ 
    a = time()
    html = urllib.request.urlopen(url).read()
    b = time()
    s = BeautifulSoup(html, "html5lib")
    c = time()
    
    print(f"{b - a:.3f}s | Downloading html \n"
          f"{c - b:.3f}s | Beautifulsoup \n"
          f"{c - a:.3f}s | Total\n")

    return s

def get_name(course):
    """ Returns the name of the course code """
    url = get_url(course)
    try:
        soup = get_soup(url);
        header = soup.body.find("main", {"class": "site-block"}).find("header")
        sv = header.find("h1").text
        en = header.find("p").text
        return sv, en
    except Exception as e:
        print(e)
        return "{} - No such course".format(course)

def print_help(args):
    print("""
    Användning: {} {{course-code ...}}

    Där `course-code' är en Lı.u kurskod från tekniska fakulteten.
    """.format(args[0]))

def main(argv):
    course_codes = map(lambda s: s.upper(), argv[1:])
    for course in course_codes:
        sv, en = get_name(course)
        print(sv.split(",")[0])


def open_course_url(course):
    url = get_url(course)
    subprocess.call("xdg-open {}".format(url), shell=True)


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ["-h", "-?", "--help"]:
        print_help(sys.argv)
        exit(1)
    else:
        [prgr, action, *rest] = sys.argv
        if action == "open":
            open_course_url(rest[0].upper())
            exit(0)

    main(sys.argv)

