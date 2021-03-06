#!/usr/bin/env python

import os
import sys
import pandas as pd
import gzip
import glob
import csv
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

INPUT_FILE = sys.argv[1]
conversions = dict()

with open(INPUT_FILE, 'r') as f:
    for line in f:
        chrom, pos, ref, alt = line.rstrip().split()
        key = ':'.join([chrom, pos, ref, alt])
        conversions[key] = " "

VCF_HEADER_RE = re.compile('^#')
dbsnp_vcf = '/lab/data/reference/human/hg19/annot/dbsnp150_variants/All_20170710.vcf.gz'

line_count = 0
with gzip.open(dbsnp_vcf, 'rt') as f:
    for line in f:
        line_count += 1
        if line_count % 5000000 == 0:
            logging.info('Processed {} lines'.format(line_count))
        if VCF_HEADER_RE.match(line):
            continue
        line = line.rstrip().split()
        chrom, pos, rsid, ref, alt = line[0:5]
        for i in alt.split(','):
            key = ':'.join([chrom, pos, ref, i])
            if key in conversions:
                conversions[key] = rsid

for key, val in conversions.items():
    chrom, pos, ref, alt = key.split(':')
    rsid = val
    print('\t'.join([chrom, pos, ref, alt, rsid]))
