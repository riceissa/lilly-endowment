#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup


def mysql_quote(x):
    """Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    our input is fixed and from a basically trustable source."""
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


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
               "date": month + "-01", "url": grant_url(focus_area, month)}


def grant_url(focus_area, month):
    """Use the focus area and donation date information to get the original grant URL."""
    fa = {
        "community-development": 13,
        "education-youth": 28,
        "religion": 11,
    }[focus_area]
    month_param = month[2:]

    return f"https://lillyendowment.org/for-current-grantees/recent-grants/?fa={fa}&date={month_param}"


def print_sql(grants_generator):
    insert_stmt = """insert into donations (donor, donee, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, url, donor_cause_area_url, notes, affected_cities) values"""
    first = True
    for grant in grants_generator:
        if first:
            print(insert_stmt)
        print(("    " if first else "    ,") + "(" + ",".join([
            mysql_quote("Lilly Endowment"),  # donor
            mysql_quote(grant["grantee"]),  # donee
            str(grant["amount"]),  # amount
            mysql_quote(grant["date"]),  # donation_date
            mysql_quote("month"),  # donation_date_precision
            mysql_quote("donation log"),  # donation_date_basis
            mysql_quote(grant["focus_area"]),  # cause_area
            mysql_quote(grant["url"]),  # url
            mysql_quote(""),  # donor_cause_area_url
            mysql_quote("Purpose: " + grant["purpose"]),  # notes
            mysql_quote(grant["grantee_location"]),  # affected_cities
        ]) + ")")
        first = False
    if not first:
        # If first is still true, that means we printed nothing above,
        # so no need to print the semicolon
        print(";")

if __name__ == "__main__":
    main()
