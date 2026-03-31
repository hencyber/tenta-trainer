#!/usr/bin/env python3
"""Fix ALL remaining missing Swedish characters in data.js"""
import sys

with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js', encoding='utf-8') as f:
    d = f.read()

fixes = [
    ('hamta', 'hämta'),('Hamta', 'Hämta'),
    ('Monsterig', 'Mönsterig'),('monsterig', 'mönsterig'),
    ('igenkanning', 'igenkänning'),
    ('radgivare', 'rådgivare'),('Radgivare', 'Rådgivare'),
    ('Bradskande', 'Brådskande'),('bradskande', 'brådskande'),
    (' kanda ', ' kända '),
    ('lakemedels', 'läkemedels'),('Lakemedels', 'Läkemedels'),
    ('ordinationsratt', 'ordinationsrätt'),
    (' na ', ' nå '),
    ('skrivrakomst', 'skrivåtkomst'),
    ('flodet', 'flödet'),('Flodet', 'Flödet'),
    ('Irreguljar', 'Irreguljär'),('irreguljar', 'irreguljär'),
    ('gora ', 'göra '),
    (' kant ', ' känt '),(' kant.', ' känt.'),
    ('mansklig', 'mänsklig'),('Mansklig', 'Mänsklig'),
    ('Kvalitetsgränskare', 'Kvalitetsgranskare'),
    ('sarskild', 'särskild'),
    ('kanslig', 'känslig'),
    ('genomfora', 'genomföra'),
    ('uppfoljning', 'uppföljning'),
    ('leverantor', 'leverantör'),('Leverantor', 'Leverantör'),
    ('avgorande', 'avgörande'),
    ('tillracklig', 'tillräcklig'),
    ('anmalan', 'anmälan'),('Anmalan', 'Anmälan'),
    ('rattsakerhet', 'rättssäkerhet'),
    ('osakerhet', 'osäkerhet'),
    ('standigt', 'ständigt'),
    ('formaga', 'förmåga'),
    (' gar ', ' går '),(' gar.', ' går.'),
    ('uppfylls', 'uppfylls'),
    ('saknar ', 'saknar '),
    ('forklara', 'förklara'),
    ('vagledning', 'vägledning'),
]

count = 0
for old, new in fixes:
    if old != new and old in d:
        c = d.count(old)
        d = d.replace(old, new)
        count += c
        print(f'  {old} -> {new} ({c}x)')

print(f'Total: {count}')
with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js', 'w', encoding='utf-8') as f:
    f.write(d)
print('Written OK')
