# Lilly Endowment

This is for the Donations List Website: https://github.com/vipulnaik/donations

Specific issue: https://github.com/vipulnaik/donations/issues/66

# How to get a new data and generate the SQL statements

NOTE: the months and focus areas are hard-coded into `wget-commands.sh`, so
before you run that script you will need to determine the new months/focus
areas and edit the relevant arrays.

```bash
today=$(date -Idate)

# Make new directory for data
mkdir data-retrieved-$today
cd data-retrieved-$today

# Download grants pages
../wget-commands.sh

# Go back up the directory tree
cd ..

# Use the HTML files to generate a SQL file containing insert statements
./proc.py data-retrieved-$today/* > out.sql
```

# License

CC0 for code.
