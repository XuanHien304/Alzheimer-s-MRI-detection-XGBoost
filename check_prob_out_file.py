import os, subprocess, re, sys 
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-fs_log_dir', help = 'Path to log file output of freesurfer')
args =parser.parse_args()
log_dir = args.fs_log_dir

def check_prob(path):
	ls_prob = []
	ls = os.listdir(path)
	for i in ls:
		with open(os.path.join(path,i)) as f:
			lines = f.readlines()
		if lines[-1] != 'done\n':
			ls_prob.append(i[:10])
	return ls_prob

if __name__ == "__main__":
	ls_prob = check_prob(log_dir)
	df = pd.DataFrame({'list of problem processes': ls_prob})
	df.to_csv(os.path.join(log_dir,'problem IDs'), index = False)
