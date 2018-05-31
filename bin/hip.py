#!/usr/bin/python
#Kate Lawrence-Gupta
#Hip.py - load gen script for splunkforwarder performance testing


# Import needed modules
import string
import datetime
import random
import time
import re


# Declare some needed variables
data = "/opt/splunkforwarder/etc/apps/hipster/default/dict"
config_file = "/opt/splunkforwarder/etc/apps/hipster/default/load.conf"
string.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Randomize!...so sparkly
y = random.choice(string.letters)
x = random.randint(1, 10)

# Open the file and get events of random length
l = open(data).read().split(y)


# Time Date stamper
def tds():
    now = datetime.datetime.now()
    return now

# Actually makes the junk
def makesomejunk(l,x):
    for i in xrange(0, len(l), x):
        yield l[i:i+x]

# Main function
def generate_load():
    for i in makesomejunk(l,x):
        for line in i:
            str(line)
            if len(line)>0:
                logme = (str(tds()) + "   " + line + '\n')
		print(logme)


# Defines the load factor from above - iterative loop
def main(n):
    while n > 0:
       generate_load()
       time.sleep(2.5)
       n = n - 1

def get_config(config_file):
    config = open(config_file).readlines()
    for i in config:
        r  = re.search('rate\s=\s+(\w+.\w+|\w+)x',i)
        if r is not None:
            rate = str(r.group())
            if "1.5" in rate:
                load_factor = 1
            if "3" in rate:
                load_factor = 2
            if "6" in rate:
                load_factor = 4
            return load_factor


if __name__ == "__main__":
        load_factor = get_config(config_file)
        main(load_factor)
