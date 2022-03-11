# Alzheimer's Detection 
data collected from: [ADNI](http://adni.loni.usc.edu/) 

Alzheimer's Disease Neuroimaging Initiative(ADNI) is a multisite study that aims to improve clinical trials for the prevention and treatment of Alzheimer’s disease.

The project is to detect Alzheimer's disease using MRI images and feature extraction applying machine learning

## Data Acquisition
The MRI scan images datasets were used from the ADNI(Alzheimer’s Disease Neuroimaging Initiative) who provide these data for research work. The dataset units comprised of .nii format (Neuroimaging Informatics Technology Initiative). This MRI data set consists typically of various combination of images representing the projection of an anatomical volume onto an image plane (projection or planar imaging), a series of images representing thin slices through a volume (tomographic or multi-slice two-dimensional imaging).

Data pre-preprocessing: FreeSurfer software was conducted to provide us the details on statistics of volume on each brain's region. The output of Freesurfer are label, mri, stat, surf, what we need is just the stats that are the features of the brain such as volume, acreage of each brain region. Collecting all to create a table called tabular dataset which is used as the data of this model. Normalization of data reduces a variety of inconsistencies which can hinder data review.

After installing Freesurfer follow the document above ans make sure your device have strong CPU with many cores to perform the tool, do these steps:

    1. export f='path/to/mri/data/file'
    
    2. bash /FreeSurfer/recon

It takes about 6 to 7 hours per image or depends on your device. Finishing, we can check output file to make sure there is no error during the process by:

``` 
python check_prob_out_file.py -fs_log_dir <path/to/output/file>
```
Next, we convert these stat files to tabular data csv file:
    
    python conver_stat_to_csv.py -fs_dir <path/output/freesurfer> -stat_dir <path/output/stat>
After that, excec_command will be collected (make sure you run separately on AD and CN groups), excec_command could be bash on Ubuntu shell, it convert stat to table file here is csv of each brain region. Finally, we got the completely csv file:
```
python collect_csv_main.py -stat_dir <path/to/final/stat>
```