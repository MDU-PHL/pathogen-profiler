#! /usr/bin/env python
import os
import sys
import argparse
import json
from collections import defaultdict
from tqdm import tqdm

def main(args):
	if args.samples:
		samples = [x.rstrip() for x in open(args.samples).readlines()]
	else:
		samples = [x.replace(".pp-results.json","") for x in os.listdir("%s/"%args.dir) if x[-13:]==".pp-results.json"]
	mutations = defaultdict(set)
	for s in tqdm(samples):
		tmp = json.load(open("%s/%s.pp-results.json" % (args.dir,s)))
		for var in tmp["dr_variants"]:
			mutations[(var["gene"],var["change"])].add(s)
		for var in tmp["other_variants"]:
			mutations[(var["gene"],var["change"])].add(s)
	num_samples = len(samples)
	if args.summary:
		O = open(args.summary,"w")
		O.write("Gene\tMutation\tFrequency\n")
		for gene,change in mutations:
			num = len(mutations[(gene,change)])
			if args.pct:
				pct = num/num_samples*100
				O.write("%s\t%s\t%s (%.2f)\n" % (gene,change,num,pct))
			else:
				O.write("%s\t%s\t%s\n" % (gene,change,num))
		O.close()
	if args.matrix:
		O = open(args.matrix,"w")
		O.write("gene\tchange\t%s\n" % ("\t".join(samples)))
		for gene,change in tqdm(mutations):
			O.write("%s\t%s\t%s\n" % (gene,change,"\t".join(["1" if s in mutations[(gene,change)] else "0" for s in samples])))
		O.close()
	if args.fasta:
		F = open(args.fasta,"w")
		for s in tqdm(samples):
			F.write(">%s\n%s\n" % (s, "".join(["1" if s in mutations[(gene,change)] else "0" for gene,change in mutations])))
		F.close()


parser = argparse.ArgumentParser(description='TBProfiler pipeline',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--samples',type=str,help='NGS Platform')
parser.add_argument('--dir',default="pp-results",type=str,help='NGS Platform')
parser.add_argument('--matrix',type=str,help='NGS Platform')
parser.add_argument('--fasta',type=str,help='NGS Platform')
parser.add_argument('--summary',type=str,help='NGS Platform')
parser.add_argument('--pct',action="store_true",help='NGS Platform')
parser.set_defaults(func=main)

args = parser.parse_args()
args.func(args)
