## vcfExporter

Convert Progenetix data to VCF

### Usage

Prepare the data in a JSON file.

```Python
import json
from vcfExporter import vcfExporter

js_file = 'progenetix_export.json'
with open(js_file, 'r') as fi:
    js = json.load(fi)

exporter = vcfExporter(js)
exporter.write('test.vcf')
```

