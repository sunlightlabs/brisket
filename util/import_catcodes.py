#!/usr/bin/python
import sys, csv, json

''' 
convert the catcode CSV file into two python dicts, keyed by industry
code and sub-industry code, respectively.

usage:
import_catcodes.py path/to/input.csv path/to/output.py 

! output.py will be overwritten if it exists.
'''


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'usage: import_catcodes.py from_file to_file'
        sys.exit()
    from_file = sys.argv[1]
    to_file = sys.argv[2]
    lines = csv.reader(open(from_file), delimiter=',', quotechar='"')
    industry = {}
    industry_area = {}
    for line in lines:
        source, code, sub_industry, ind, order = line
        industry[order] = (ind, sub_industry)
        industry_area[code] = (ind, sub_industry)

    sectors = {
        'F': 'Finance/Insurance/Real Estate',
        'A': 'Agribusiness',
        'W': 'Other',
        'Q': 'Ideology/Single Issue',
        'N': 'Misc. Business',
        'K': 'Lawyers and Lobbyists',
        'H': 'Health',
        'B': 'Communications/Electronics',
        'C': 'Construction',
        'E': 'Energy/Natural Resources',
        'P': 'Labor',
        'M': 'Transportation',
        'D': 'Defense',        
        'Z': 'Administrative', 
        'Y': 'Unknown', 
        }

    out = open(to_file, 'w')
    out.write("industry = ")
    json.dump(industry, out)
    out.write("\nindustry_area = ")
    json.dump(industry_area, out)
    out.write("\nsector = ")
    json.dump(sectors, out)
    out.close()
