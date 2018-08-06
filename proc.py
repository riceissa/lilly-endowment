#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup


def main():
    print(sys.argv)
    for filepath in sys.argv[1:]:
        with open(filepath, "r") as f:
            filename = filepath.split("/")[-1]
            soup = BeautifulSoup(f, "lxml")
            month = filename[:len("YYYY-MM")]
            focus_area = filename[len("YYYY-MM-"):].split(".")[0]
            soup_to_grants_list(soup, focus_area, month)


def soup_to_grants_list(soup, focus_area, month):
    for grantee_div in soup.find("div", {"class": "grants-archive-inner"}).find_all("div", {"class": "grantee"}):
        grantee = grantee_div.find("div", {"class": "grantee-name"}).text
        info = grantee_div.find("div", {"class": "grantee-info"}).text
        grantee_location, amount = info.split("•")
        purpose = grantee_div.find("div", {"class": "grantee-purpose"}).text
        print(month, focus_area, grantee, amount)


if __name__ == "__main__":
    main()
