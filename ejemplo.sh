#!/bin/bash

database=$1
val=$2

cp get_results.sql get_results_temp.sql
sed -i "s/REMPLAZAR/$1/g" get_results_temp.sql
sudo mysql -u root -p$3 -e "source get_results_temp.sql"
sudo mysql -u root -p$3 -e "call $database.get_folder_results($val)"
rm get_results_temp.sql



