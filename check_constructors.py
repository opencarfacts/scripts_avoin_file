#!/usr/bin/python
# -*- coding: utf8 -*-
import csv
import sys
import operator

if len(sys.argv) != 2:
    print "Usage python check_constructor.py name_file"

print "Filename: {}".format(sys.argv[1])

fieldnames=['category', 'first_registration_date', 'classification',
            'usage', 'first_use_date', 'colour', 'nb_doors', 'body_type',
            'cab_type', 'nb_seats', 'weight', 'max_mass', 'max_mass_road',
            'length', 'width', 'height', 'power', 'cylinder_capacity',
            'max_power', 'nb_cylinders', 'ahdin', 'hybrid', 'constructor',
            'designation', 'transmission_type', 'nb_forward_gears',
            'commercial_name', 'method', 'type_id_number', 'driving_power',
            'municipality', 'co2', 'nb_kilometers', 'post_code', '10_vin',
            'sequential_numbering']
map_wmi_constructor = {
    'AAV': ['Volkswagen'],
    'AFA': ['Ford'],
    'CL9': ['Wallyscar'],
    'JA': ['Isuzu'],
    'JF': ['Fuji Heavy Industries', 'fuji'],
    'JH': ['Honda'],
    'JMB': ['Mitsubishi'],
    'JMZ': ['Mazda'],
    'JN': ['Nissan'],
    'JS': ['Suzuki'],
    'JT': ['Toyota'],
    'KL': ['Daewoo/GM Korea', 'daewoo', 'gm korea'],
    'KMH': ['Hyundai'],
    'KN': ['Kia'],
    'KPT': ['SsangYong'],
    'LVZ': ['DFSK'],
    'NMT': ['Toyota'],
    'SAJ': ['Jaguar'],
    'SAL': ['Land Rover', 'landrover'],
    'SAR': ['Rover'],
    'SB1': ['Toyota'],
    'SCC': ['Lotus Cars', 'lotus'],
    'SCE': ['DeLorean'],
    'SHH': ['Honda'],
    'SJN': ['Nissan'],
    'TMA': ['Hyundai'],
    'TMB': ['Škoda', 'skoda'],
    'TRU': ['Audi'],
    'UU': ['Dacia'],
    'VA0': ['ÖAF', 'oaf'],
    'VF1': ['Renault'],
    'VF3': ['Peugeot'],
    'VF6': ['Renault Trucks/Volvo', 'renault'],
    'VF7': ['Citroën', 'citroen'],
    'VFE': ['IvecoBus'],
    'VSS': ['SEAT'],
    'VV9': ['Tauro Sport Auto'],
    'WAU': ['Audi'],
    'WAP': ['Alpina'],
    'WBA': ['BMW'],
    'WBS': ['BMW M', 'bmw'],
    'WDB': ['Mercedes-Benz'],
    'WDC': ['DaimlerChrysler AG/Daimler AG', 'daimler', 'chrysler', 'daimlerchrysler'],
    'WDD': ['DaimlerChrysler AG/Daimler AG', 'daimler', 'chrysler', 'daimlerchrysler'],
    'WMX': ['DaimlerChrysler AG/Daimler AG', 'daimler', 'chrysler', 'daimlerchrysler'],
    'WEB': ['EvoBus'],
    'WF0': ['Ford of Europe', 'ford'],
    'WJM': ['Iveco'],
    'WJR': ['Irmscher'],
    'WKK': ['Kässbohrer', 'kassbohrer'],
    'WMA': ['MAN'],
    'WME': ['Smart'],
    'WMW': ['Mini'],
    'WP0': ['Porsche car', 'porsche'],
    'WP1': ['Porsche SUV', 'porsche'],
    'WUA': ['Quattro'],
    'WVG': ['Volkswagen'],
    'WVW': ['Volkswagen'],
    'WV1': ['Volkswagen Commercial Vehicles', 'volkswagen'],
    'WV2': ['Volkswagen Commercial Vehicles', 'volkswagen'],
    'W0L': ['Opel/Vauxhall', 'opel'],
    'W0SV': ['Opel Special Vehicles', 'opel'],
    'YK1': ['Saab'],
    'YS3': ['Saab'],
    'YTN': ['Saab NEVS', 'saab'],
    'YV1': ['Volvo Cars', 'volvo'],
    'ZAM': ['Maserati'],
    'ZAR': ['Alfa Romeo', 'alfa', 'alfaromeo'],
    'ZCF': ['Iveco'],
    'ZFA': ['Fiat Automobiles', 'fiat'],
    'ZFF': ['Ferrari'],
    'ZGA': ['IvecoBus'],
    'ZHW': ['Lamborghini'],
    'ZLA': ['Lancia'],
    '1B': ['Dodge'],
    '1C': ['Chrysler'],
    '1F': ['Ford'],
    '1G': ['General Motors', 'generalmotors', 'gm'],
    '1G3': ['Oldsmobile'],
    '1GC': ['Chevrolet'],
    '1GM': ['Pontiac'],
    '1H': ['Honda'],
    '1J': ['Jeep'],
    '1L': ['Lincoln'],
    '1M': ['Mercury'],
    '1N': ['Nissan'],
    '1VW': ['Volkswagen'],
    '1YV': ['Mazda'],
    '2F': ['Ford'],
    '2G': ['General Motors'],
    '2G1': ['Chevrolet'],
    '2G2': ['Pontiac'],
    '2H': ['Honda'],
    '2HM': ['Hyundai'],
    '2M': ['Mercury'],
    '2T': ['Toyota'],
    '3F': ['Ford'],
    '3G': ['General Motors'],
    '3H': ['Honda'],
    '3N': ['Nissan'],
    '3VW': ['Volkswagen'],
    '4F': ['Mazda'],
    '4J': ['Mercedes-Benz'],
    '4M': ['Mercury'],
    '4S': ['Subaru'],
    '4T': ['Toyota'],
    '4US': ['BMW'],
    '5F': ['Honda'],
    '5L': ['Lincoln'],
    '5T': ['Toyota'],
    '5X': ['Hyundai/Kia', 'hyundai', 'kia'],
    '5YJ': ['Tesla'],
    '6F': ['Ford'],
    '6G': ['General Motors', 'generalmotors', 'gm'],
    '6G1': ['Chevrolet'],
    '6G2': ['Pontiac'],
    '6H': ['Holden'],
    '6MM': ['Mitsubishi'],
    '6T1': ['Toyota'],
    '8AP': ['Fiat'],
    '8AT': ['Iveco'],
    '9BD': ['Fiat Automóveis', 'fiat'],
    '9BW': ['Volkswagen'],
    '93H': ['Honda'],
    '93W': ['Fiat Professional', 'fiat'],
    '93Z': ['Iveco'],
    '9BH': ['Hyundai']}

constructors = set([s.lower() for s in reduce(operator.add, map_wmi_constructor.values())])

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
        for i in xrange(2, 5):
            constructor = map_wmi_constructor.get(vin[:i].upper(), None)
            if not constructor:
                continue
            able_to_find_vin += 1
            if constructor[0].lower() == row['constructor'].lower():
                matching_vin_constructor += 1
                continue
            if row['constructor'].lower() in constructor:
                nearly_matching_vin_constructor += 1
                continue
            if row['constructor'].lower() in constructors:
                not_matching_but_present += 1
            set_unfound_constructors.add((vin, row['constructor'].lower()))


with open('/tmp/constructors.unfound', 'wb') as constructor_file:
    for c in set_unfound_constructors:
        constructor_file.write("{}, {}\n".format(vin, c))

print "Nb empty constructors: {}".format(empty_constructors)
print "Nb empty vin: {}".format(empty_vin)
print "Nb empty vin_constructors: {}".format(empty_vin_constructor)
print "Nb able_to_find_vin: {}".format(able_to_find_vin)
print "Nb matching_vin_constructor: {}".format(matching_vin_constructor)
print "Nb nearly_matching_vin_constructor: {}".format(nearly_matching_vin_constructor)
print "There are {} constructors not found, the list has been exported to /tmp/constructors".format(len(set_unfound_constructors))
print "Nb of bad vin: {}".format(not_matching_but_present)

