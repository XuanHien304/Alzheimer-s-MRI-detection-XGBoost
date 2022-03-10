import os, subprocess, re, traceback, sys
import collections, pickle
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-fs_dir', help = 'Path to output of freesurfer')
parser.add_argument('-stat_dir', help = 'Path to output of convert stat to csv') # Check stat_dir must be empty 
# parser.add_argument('-save_table', help = 'Path to save table to, contain all stats')

args =parser.parse_args()
fs_dir = args.fs_dir
stat_dir = args.stat_dir
# out_dir = args.out_dir



def output_aparc_commands(output_file, subjfile, hemi, meas, tablefile, pattern=1, stats=None):
    if pattern == 1:
        aparc_command_pattern = """
            aparcstats2table \
            -s {} \
            --hemi {} \
            --meas {} \
            --skip \
            --delimiter comma \
            --tablefile {}
        """
        exec_command = aparc_command_pattern.format(subjfile, hemi, meas, tablefile)
    elif pattern == 2:
        aparc_command_pattern = """
            aparcstats2table \
            --parcs-from-file {} \
            -s {} \
            --hemi {} \
            --meas {} \
            --skip \
            --delimiter comma \
            --tablefile {}
        """
        exec_command = aparc_command_pattern.format(stats, subjfile, hemi, meas, tablefile)
    
    # write commands to file    
    output_file.writelines(exec_command)

def output_aseg_commands(output_file, subjfile, tablefile):
#     aseg_command_pattern = """
#         asegstats2table \
#         -s {} \
#         --statsfile={} \
#         --skip \
#         --delimiter comma \
#         --tablefile {}
#     """
    aseg_command_pattern = """
        asegstats2table \
        -s {} \
        --meas volume \
        --skip \
        --delimiter comma \
        --tablefile {}
    """
    exec_command = aseg_command_pattern.format(subjfile, tablefile)
    
    # write commands to file    
    output_file.writelines(exec_command)



def pre_convert(fs_dir, stat_dir):
    ls_sub = os.listdir(fs_dir)
    ls_sub = [subj for subj in ls_sub if subj not in ["fsaverage"]]
    # Check if stat_dir not empty
    ls_sdir = os.listdir(stat_dir)
    if len(ls_sdir) == 0:
        for i in ls_sub:
            os.system("mkdir {}".format(os.path.join(stat_dir,i)))
            os.system("chmod 777 -R {}".format(os.path.join(stat_dir,i)))
    else:
        print('Stats directory is not empty, do you want to remove {}'.format(ls_sdir))
        a = input("yes/no: ")
        if a == 'yes':
            for i in ls_sdir:
                if os.path.isdir(stat_dir + '/' + i):
                    os.system("rm -R {}".format(os.path.join(stat_dir, i)))
                else:
                    os.system("rm {}".format(os.path.join(stat_dir, i)))
        else:
            pass

    return ls_sub 

#exec_command_aparc_area_in_mm2
def aparc_area_in_mm2(ls_sub, fs_dir, stat_dir):
    
    with open("exec_command_aparc_area_in_mm2.sh", "w") as output_file:

        for i in ls_sub:
            subjfile = os.path.join(fs_dir, i)
            subj_path = os.path.join(stat_dir, i)
        
            meas = "area"
            for hemi in ["lh", "rh"]:
                tablefile = "{}/aparc-{}-{}-stats.csv".format(subj_path, meas, hemi)
                output_aparc_commands(output_file, subjfile, hemi, meas, tablefile)


#exec_command_aparc_volume_in_mm3
def aparc_volume_in_mm3(ls_sub, fs_dir, stat_dir):
    with open("exec_command_aparc_volume_in_mm3.sh", "w") as output_file:
    
        for i in ls_sub:
            subjfile = os.path.join(fs_dir, i)
            subj_path = os.path.join(stat_dir, i)

        
            meas = "volume"
            for hemi in ["lh", "rh"]:
                tablefile = "{}/aparc-{}-{}-stats.csv".format(subj_path, meas, hemi)
                output_aparc_commands(output_file, subjfile, hemi, meas, tablefile) 


#exec_command_aparc_white_matter_volume_in_mm3
def aparc_white_matter_volume_in_mm3(ls_sub,fs_dir,stat_dir):
    with open("exec_command_aparc_white_matter_volume_in_mm3.sh", "w") as output_file:
    
        for i in ls_sub:
            subjfile = os.path.join(fs_dir, i)
            subj_path = os.path.join(stat_dir, i)

        
            meas = "volume"
            wmstats = os.path.join(subjfile, "stats", "wmparc.stats")
            for hemi in ["lh", "rh"]:
                tablefile = "{}/wmparc-{}-{}-stats.csv".format(subj_path, meas, hemi)
                output_aparc_commands(output_file, subjfile, hemi, meas, tablefile, pattern=2, stats=wmstats)


#exec_command_aparc_cortical_thickness_in_mm
def aparc_cortical_thickness_in_mm(ls_sub, fs_dir, stat_dir):
    with open("exec_command_aparc_cortical_thickness_in_mm.sh", "w") as output_file:
    
        for i in ls_sub:
            subjfile = os.path.join(fs_dir, i)
            subj_path = os.path.join(stat_dir, i)

        
            meas = "thickness"
            for hemi in ["lh", "rh"]:
                tablefile = "{}/aparc-{}-{}-stats.csv".format(subj_path, meas, hemi)
                output_aparc_commands(output_file, subjfile, hemi, meas, tablefile)


#exec_command_aparc_mean_curvature
def aparc_mean_curvature(ls_sub, fs_dir, stat_dir):
    with open("exec_command_aparc_mean_curvature.sh", "w") as output_file:
    
        for i in ls_sub:
            subjfile = os.path.join(fs_dir, i)
            subj_path = os.path.join(stat_dir, i)
        
            meas = "meancurv"
            for hemi in ["lh", "rh"]:
                tablefile = "{}/aparc-{}-{}-stats.csv".format(subj_path, meas, hemi)
                output_aparc_commands(output_file, subjfile, hemi, meas, tablefile)

#exec_command_aseg_volumne
def aseg_volumne(ls_sub, fs_dir, stat_dir):

    with open("exec_command_aseg_volume.sh", "w") as output_file:
    
        for i in ls_sub:
            subjfile = os.path.join(fs_dir, i)
            subj_path = os.path.join(stat_dir, i)
        
        # TODO: investigate run segmentHA_1.sh, segmentSF_1.sh
#         for hemi in ["lh", "rh"]:
#             hippostats = os.path.join(subjfile, "stats", "hipposubfields.{}.T1.v21.stats".format(hemi))
#             tablefile = "{}/hipposubfields-{}-stats.csv".format(subj_path, hemi)
#             output_aseg_commands(output_file, hippostats, tablefile)

        # temporary use WRONG stats
            tablefile = "{}/aseg-volume-stats.csv".format(subj_path)
            output_aseg_commands(output_file, subjfile, tablefile)

def collect_csv(stat_dir):

    ls_must_have = ['aparc-area-lh-stats.csv', 
        'aparc-area-rh-stats.csv', 
        'aparc-meancurv-lh-stats.csv', 
        'aparc-meancurv-rh-stats.csv', 
        'aparc-thickness-lh-stats.csv', 
        'aparc-thickness-rh-stats.csv', 
        'aparc-volume-lh-stats.csv', 
        'aparc-volume-rh-stats.csv', 
        'aseg-volume-stats.csv']

    ls_sub = subprocess.check_output(["ls", stat_dir]).decode("utf-8").splitlines()
    ls_path = []

    for i in ls_sub:
        ls_path.append(os.path.join(stat_dir,i))
    pdf_subj = pd.DataFrame({'subj_id': ls_sub, 'subj_path': ls_path})
    dsname2cname = collections.OrderedDict()
    pdf_combine = pdf_subj[["subj_id"]].copy()
    for stats_name in ls_must_have:
        if stats_name in ['wmparc-volume-lh-stats.csv', 'wmparc-volume-rh-stats.csv']:
            continue
        
        prefix = stats_name[:-4]
        ls_pdf01 = []
        print("Extracting features: {}".format(prefix))

        for idx, pdf01 in pdf_subj.iterrows():
        
            # get info
            subj_id = pdf01["subj_id"]
            subj_path = pdf01["subj_path"]
        
            # load stats
            stats_path = os.path.join(subj_path, stats_name)
            pdf_fts = pd.read_csv(stats_path)
        
            # extract features                
            ls_cname = [name for name, dtype in pdf_fts.dtypes.items() if dtype == "float64"]
            rename_prefix = {cname: "{}_{}".format(prefix, cname) for cname in ls_cname}
        
            pdf_fts.rename(columns=rename_prefix, inplace=True)
            pdf_fts["subj_id"] = subj_id    
            ls_fts = sorted(list(rename_prefix.values()))
            pdf_fts = pdf_fts[["subj_id"] + ls_fts]
        
            # add record
            ls_pdf01.append(pdf_fts)

            # update dsname2cname
            if prefix not in dsname2cname:
                dsname2cname[prefix] = ls_fts
            
        pdf02 = pd.concat(ls_pdf01).reset_index(drop=True)
        pdf_combine = pdf_combine.merge(pdf02, on="subj_id")
        print("No. fts: {}".format(len(dsname2cname[prefix])))
        print("Combined: {}".format(pdf_combine.shape[1]))
    pdf_report = pd.DataFrame({"dsname": list(dsname2cname.keys()), "num_fts": [len(dsname2cname[dsname]) for dsname in dsname2cname]})
    print("Total features: {}".format(pdf_report["num_fts"].sum()))

    return pdf_combine


if __name__ == "__main__":
    ls_sub = pre_convert(fs_dir, stat_dir)
    aparc_area_in_mm2(ls_sub,fs_dir,stat_dir)
    aparc_volume_in_mm3(ls_sub,fs_dir,stat_dir)
    aparc_white_matter_volume_in_mm3(ls_sub,fs_dir,stat_dir)
    aparc_cortical_thickness_in_mm(ls_sub,fs_dir,stat_dir)
    aparc_mean_curvature(ls_sub,fs_dir,stat_dir)
    aseg_volumne(ls_sub,fs_dir,stat_dir)
