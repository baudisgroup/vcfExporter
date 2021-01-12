import os


class vcfExporter:
    """Convert Progenetix data to VCF"""

    def __init__(self, json_file, header_file = os.path.join(os.path.dirname(__file__),'./default_header.vcf')):
        """
        Parameters
        ----------
        json_file: str
            Progenetix data in JSON format
        header_file: str
            The header of the output VCF
        """


        self.table = {}
        self.callsets = []
        self.header_file = header_file

        # Read and parse the JSON data
        for var in json_file:
            digest = var['digest']
            
            if var['reference_name'] in ['X', 'Y']:
                gt = '.'
            else:
                gt = './.'
            if var['info']['cnv_value'] != None:
                cn = var['info']['cnv_value']
            else:
                cn = ''
            
            fmt = '{}:{}'.format(gt,cn)
            
            if digest not in self.table.keys():
                self.table[digest] = {}
                
                if var['reference_name'] == 'X':
                    int_chrom = 23
                elif var['reference_name'] == 'Y':
                    int_chrom = 24
                else:
                    int_chrom = int(var['reference_name'])
                
                self.table[digest]['INTCHROM'] = int_chrom 
                self.table[digest]['CHROM'] = var['reference_name']
                self.table[digest]['POS'] = str(var['start'])
                self.table[digest]['END'] = str(var['end'])
                self.table[digest]['ID'] = digest
                self.table[digest]['REF'] = 'N'
                self.table[digest]['ALT'] = '<{}>'.format(var['variant_type'])
                self.table[digest]['QUAL'] = '.'
                self.table[digest]['FILTER'] = 'PASS'
                self.table[digest]['INFO'] = 'SVTYPE=CNV;END={};REFLEN={}'.format(var['end'], var['info']['cnv_length'])
                self.table[digest]['FORMAT'] = 'GT:CN'
                self.table[digest]['callsets'] = {var['callset_id']:fmt}
            else:
                self.table[digest]['callsets'][var['callset_id']] = fmt
            
            if var['callset_id'] not in self.callsets:
                self.callsets.append(var['callset_id'])
    
    def gen_colnames(self):
        """ Generate column names for the VCF output"""

        colnames = '\t'.join(['CHROM',
                        'POS',
                        'ID',
                        'REF',
                        'ALT',
                        'QUAL',
                        'FILTER',
                        'INFO',
                        'FORMAT'])
        callnames = '\t'.join(self.callsets)
        return '{}\t{}'.format(colnames, callnames)    

    def write(self, output):
        """ Write the Progenetix data into a standard VCF

        Parameters:
        output: str
            The output path
        """

        with open(output, 'w') as fo, open(self.header_file, 'r') as fh:
            # wrtie headers
            fo.writelines(l for l in fh)
            # write column names
            fo.write(self.gen_colnames() + '\n')
            
            # write data
            for k  in sorted(self.table, key=lambda x: (self.table[x]['INTCHROM'], self.table[x]['POS'], self.table[x]['END'], self.table[x]['ALT'])):
            
                mute = '\t'.join([self.table[k]['CHROM'],
                                self.table[k]['POS'],
                                self.table[k]['ID'],
                                self.table[k]['REF'],
                                self.table[k]['ALT'],
                                self.table[k]['QUAL'],
                                self.table[k]['FILTER'],
                                self.table[k]['INFO'],
                                self.table[k]['FORMAT']])


                if self.table[k]['CHROM'] in ['X', 'Y']: 
                    calls = ['0:.']*len(self.callsets)
                else:
                    calls = ['0/0:.']*len(self.callsets)
                for cs, v in self.table[k]['callsets'].items():
                    index = self.callsets.index(cs)
                    calls[index] = v

                fo.write('\t'.join([mute, '\t'.join(calls)]) + '\n')
