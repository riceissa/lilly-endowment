#!/bin/bash

declare -a months=("17-01" "17-02" "17-03" "17-04" "17-05" "17-06" "17-07" "17-08" "17-09" "17-10" "17-11" "17-12")
declare -A focusareas=(["13"]="community-development" ["28"]="education-youth" ["11"]="religion")

for focusarea in "${!focusareas[@]}"; do
    for month in "${months[@]}"; do
        wget -U 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' "https://lillyendowment.org/for-current-grantees/recent-grants/?fa=${focusarea}&date=${month}" -O "20${month}-${focusareas[${focusarea}]}.html"
    done
done
