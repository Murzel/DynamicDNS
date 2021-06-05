import re

def find_ip(string : str) -> str:
    if (tmp := re.search(r'[0-9]+.[0-9]+.[0-9]+.[0-9]+', string)):
        return tmp.string

    return ""

def listToDict(devidor, array) -> dict:
    tmp = {}

    for arr in array:
        pos = arr.find(devidor)
        tmp[arr[:pos]] = arr[pos+1:].strip()

    return tmp