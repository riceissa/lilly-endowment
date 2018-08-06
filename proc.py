#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup


def main():
    for filepath in sys.argv[1:]:
        with open(filepath, "r") as f:
            filename = filepath.split("/")[-1]
            soup = BeautifulSoup(f, "lxml")

            # The donation date and focus area information are not in
            # the HTML so we get them from the filename
            month = filename[:len("YYYY-MM")]
            focus_area = filename[len("YYYY-MM-"):].split(".")[0]

            print_sql(soup_to_grants_generator(soup, focus_area, month))


def soup_to_grants_generator(soup, focus_area, month):
    for grantee_div in soup.find("div", {"class": "grants-archive-inner"}).find_all("div", {"class": "grantee"}):
        grantee = grantee_div.find("div", {"class": "grantee-name"}).text
        info = grantee_div.find("div", {"class": "grantee-info"}).text
        grantee_location, amount = info.split("•")
        amount = float(amount.replace("$", "").replace(",", ""))
        purpose = grantee_div.find("div", {"class": "grantee-purpose"}).text

        focus_area_map = {
            "community-development": "Community development",
            "education-youth": "Education/Youth",
            "religion": "Religion",
            }
        yield {"grantee": grantee, "grantee_location": grantee_location,
               "amount": amount, "purpose": purpose,
               "focus_area": focus_area_map[focus_area],
               "date": month + "-01"}


def print_sql(grants_generator):
    for grant in grants_generator:
        print(grant)

if __name__ == "__main__":
    main()
