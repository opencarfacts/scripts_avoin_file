#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os, csv, operator
from unidecode import unidecode

if len(sys.argv) != 2:
    print "Usage python check_constructor.py name_file"


fieldnames=['category', 'first_registration_date', 'classification',
            'usage', 'first_use_date', 'colour', 'nb_doors', 'body_type',
            'cab_type', 'nb_seats', 'weight', 'max_mass', 'max_mass_road',
            'length', 'width', 'height', 'power', 'cylinder_capacity',
            'max_power', 'nb_cylinders', 'ahdin', 'hybrid', 'constructor',
            'designation', 'transmission_type', 'nb_forward_gears',
            'commercial_name', 'method', 'type_id_number', 'driving_power',
            'municipality', 'co2', 'nb_kilometers', 'post_code', '10_vin',
            'sequential_numbering']

map_wmi_constructor = {}
map_constructor_aliases = {}
map_constructor_wmi = {}
map_constructor_no_set = {}
p = 'wmi_constructors'
for constructor in [f for f in os.listdir(p) if os.path.isdir(os.path.join(p, f))]:
    map_constructor_wmi[constructor] = set()
    map_constructor_no_set[constructor] = set()
    constructor_path = os.path.join(p, constructor)
    map_constructor_aliases[constructor] = set()
    for wmi in [f for f in os.listdir(constructor_path) if os.path.isfile(os.path.join(constructor_path, f))]:
        with open(os.path.join(p, constructor, wmi), 'r+') as file_:
            if wmi == 'aliases':
                for l in file_:
                    if len(l.strip()) == 0:
                        continue
                    map_constructor_aliases[constructor].add(l.strip())
                continue
            map_constructor_wmi[constructor].add(wmi)
            map_wmi_constructor[wmi] = constructor
            for l in file_:
                if len(l) == 0:
                    continue
	        map_constructor_aliases[constructor].add(l.strip())
aliases = set([s.lower() for s in reduce(set.union, map_constructor_aliases.values())])

with open(sys.argv[1], 'rb') as csvfile:
    i = 0

    vehicles_reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    empty_constructors = 0
    empty_vin = 0
    empty_vin_constructor = 0
    able_to_find_vin = 0
    matching_vin_constructor = 0
    nearly_matching_vin_constructor = 0
    not_matching_but_present = 0
    j = 0
    set_unfound_constructors = set()
    for row in vehicles_reader:
        i += 1
        if not row['constructor']:
            empty_constructors += 1
        if not row['10_vin']:
            empty_vin += 1
            if not row['constructor']:
                empty_vin_constructor += 1
            continue
        vin = row['10_vin']
        constructor = ""
        quit = False
        for i in xrange(2, 5):
            wmi = vin[:i].upper()
            constructor = map_wmi_constructor.get(wmi, None)
            if not constructor:
                continue
            aliases_list = map_constructor_aliases[constructor]
            able_to_find_vin += 1
            raw_constructor = unidecode(unicode(row['constructor'], 'utf-8')).lower()
            if map_wmi_constructor[wmi].lower() == raw_constructor:
                matching_vin_constructor += 1
                continue
            if raw_constructor in aliases_list:
                nearly_matching_vin_constructor += 1
                continue
            if raw_constructor in aliases:
                not_matching_but_present += 1
            no_set = map_constructor_no_set[constructor]
            if raw_constructor in no_set:
                continue
            print "We found the WMI code, but we are unable to find a matching constructor"
            print "List of aliases: {}".format(aliases_list)
            print "Do you want to add {} as an alias for this constructor: {}".format(raw_constructor,
		map_wmi_constructor[wmi])
            input_ = raw_input("y/n/q")
            print "{} {}".format(input_, (input_=="y"))
            if input_ == "y":
		ref_constructor = map_wmi_constructor[wmi]
		map_constructor_aliases[ref_constructor].add(raw_constructor)
                continue
                
            if input_ == "q":
                quit = True
                break

            if input_ == "n":
                map_constructor_no_set[constructor].add(raw_constructor)
            set_unfound_constructors.add((vin[:4], row['constructor']))
        if quit:
            break


with open('/tmp/constructors.unfound', 'wb') as constructor_file:
    for c in set_unfound_constructors:
        constructor_file.write("{}, {}\n".format(c[0], c[1]))

for constructor, aliases in map_constructor_aliases.iteritems():
    with open(os.path.join('wmi_constructors', constructor, 'aliases'), 'wb') as aliases_file:
	for alias in aliases:
	    aliases_file.write("{}\n".format(alias))

print "Nb empty constructors: {}".format(empty_constructors)
print "Nb empty vin: {}".format(empty_vin)
print "Nb empty vin_constructors: {}".format(empty_vin_constructor)
print "Nb able_to_find_vin: {}".format(able_to_find_vin)
print "Nb matching_vin_constructor: {}".format(matching_vin_constructor)
print "Nb nearly_matching_vin_constructor: {}".format(nearly_matching_vin_constructor)
print "There are {} constructors not found, the list has been exported to /tmp/constructors".format(len(set_unfound_constructors))
print "Nb of bad vin: {}".format(not_matching_but_present)

