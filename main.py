#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
import re
import sys

institutions = {
        "A": "MAI",
        "D": "IDA",
        "S": "ISY",
        "F": "IFM"
        }

urls = {
        "MAI": "http://courses.mai.liu.se/GU/{}/",
        "IDA": "https://www.ida.liu.se/~{}/index.sv.shtml",
        "ISY": "http://www.isy.liu.se/edu/kurs/{}/",
        "IFM": "https://www.ifm.liu.se/edu/coursescms/{}/",
        }

transformers = {
        "MAI": lambda x: x,
        "IDA": lambda x: x,
        "ISY": lambda x: x,
        "IFM": lambda x: x.lower()
        }      


def get_url(course_code):
    inst = institutions[course_code[1]]
    return urls[inst].format(transformers[inst](course_code))

def get_soup(url):
    html = urllib.request.urlopen(url).read()
    return BeautifulSoup(html, "html5lib")

def get_name(course):
    url = get_url(course)
    try:
        soup = get_soup(url);
        return soup.body.findAll("h1", text=re.compile(course))[0].text.strip()
    except Exception:
        return "{} - No such course".format(course)

def print_help(args):
    print("""
    Användning: {} {{course-code ...}}

    Där `course-code' är en Lı.u kurskod från tekniska fakulteten.
    """.format(args[0]))

def main(argv):
    course_codes = map(lambda s: s.upper(), argv[1:])
    for course in course_codes:
        print(get_name(course))

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ["-h", "-?", "--help"]:
        print_help(sys.argv)
        exit(1)
    main(sys.argv)

