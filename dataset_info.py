#Import the libraries we are going to use
import os
import pandas as pd
import pandas_profiling
import shutil

#Set the data folder in which you have the csv files and the folder to save the html files (Create them previously)
PATH = './data/'
PATH_output_file = './html/'
PATH_processed_file = './processed/'

#Read all files on data folder
datasets_list = os.listdir(PATH)
print('Analyzing {} datasets...'.format(len(datasets_list)))

#Read each file as a dataframe and profile it with ProfileReport function
for dataset in datasets_list:
    dataframe = pd.read_csv(PATH + dataset,sep = '|', encoding = 'iso-8859-1')
    print('-----------' + dataset + '-----------')
    print(dataframe.info())
    print('Creating HTML overview...')
    dataframe_profiling = pandas_profiling.ProfileReport(dataframe)
    dataframe_profiling.to_file(PATH_output_file + dataset[:-3] + 'html')
    shutil.move(PATH + dataset, PATH_processed_file + dataset)