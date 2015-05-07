#!/bin/bash
echo $1
finalname="$1.utf8"
finalnametmp="$finalname.tmp"

echo $finalname

iconv -f ISO-8859-1 -t UTF-8  $1 -o $finalname

sed "1s/.*/category,first_registration_date,classification,usage,first_use_date,colour,nb_doors,body_type,cab_type,nb_seats,weight,max_mass,max_mass_road,length,width,height,power,cylinder_capacity,max_power,nb_cylinders,ahdin,hybrid,constructor,designation,transmission_type,nb_forward_gears,commercial_name,method,type_id_number,driving_power,municipality,co2,nb_kilometers,post_code,10_vin,sequential_numberin/" $finalname > $finalnametmp
mv $finalnametmp $finalname
