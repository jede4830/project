import requests
import json
import time
import urllib
from sys import argv
from tools import get_continuation_from_number, get_patent_numbers_from_list

def main():
    a = get_continuation_from_number(argv[1])
    numlist = get_patent_numbers_from_list( a )
    print(numlist)

if __name__=='__main__':
    main()

