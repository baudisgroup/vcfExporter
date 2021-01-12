import sys
sys.path.append("..")

import json
from vcfExporter import vcfExporter

js_file = '/Users/bogao/DataFiles/vcfexporter_test_1.json'
with open(js_file, 'r') as fi:
    js = json.load(fi)

exporter = vcfExporter(js)
exporter.write('test.vcf')