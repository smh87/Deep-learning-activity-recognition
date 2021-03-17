import os
import csv
from dotenv import load_dotenv
from shutil import copy2


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  
def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]

load_dotenv()
datafile_Path = os.getenv('DATAFILE_PATH') #Change this to your file location
if datafile_Path == 'missing':
    print('Set the path to your dataset in the .env')
    exit()
new_datafile_path = datafile_Path + '\\formattet_dataset_uci'

files = {
    'final_acc_train.txt',
    'final_gyro_train.txt',
    'final_X_train.txt',
    'final_y_train.txt',
    'final_acc_test.txt',
    'final_gyro_test.txt',
    'final_X_test.txt',
    'final_y_test.txt',
    'features.txt',
    'activity_labels.txt'
}


try: #create folder
    os.mkdir(new_datafile_path)
except OSError as e:
    print(e)
    print ('Creation of new dataset folder failed')
    exit()
else:
    print('New dataset folder created')

try: #create test folder 
    os.makedirs(new_datafile_path + '\\test\\Inertial Signals')
except OSError as e:
    print(e)
    print ('Creation of \\test\\Inertial Signals failed')
    exit()
else:
    print('New dataset folder created')

try:  #create train folder
    os.makedirs(new_datafile_path + '\\train\\Inertial Signals')
except OSError as e:
    print(e)
    print ('Creation of \\train\\Inertial Signals failed')
    exit()
else:
    print('New dataset folder created')

for file in files:
    temp_file = remove_prefix(file, 'final_')
    if 'test' in file or 'train' in file:
        path = ''
        if 'test' in file:
            path = new_datafile_path + '\\test\\'
        elif 'train' in file:
            path = new_datafile_path + '\\train\\'
        if 'acc' in file or 'gyro' in file:
            path = path + 'Inertial Signals\\'
            temp_file =  remove_suffix(temp_file, '.txt')
            splitfile = temp_file.split('_')
            splitfile[0] = 'body_' + splitfile [0]
            x_path = path + splitfile[0] + '_x_' + splitfile[1] + '.txt'
            y_path = path + splitfile[0] + '_y_' + splitfile[1] + '.txt'
            z_path = path + splitfile[0] + '_z_' + splitfile[1] + '.txt'
            x_file = open(x_path, 'w')
            y_file = open(y_path, 'w')
            z_file = open(z_path, 'w')
            with open(datafile_Path + '\\dataset_uci\\' + file, 'rt') as f:
                data = csv.reader(f)
                i = 0
                for row in data:
                    x_file.write(' ' + row[0] if row[0].startswith('-') else '  ' + row[0])
                    y_file.write(' ' + row[1] if row[1].startswith('-') else '  ' + row[1])
                    z_file.write(' ' + row[2] if row[2].startswith('-') else '  ' + row[2])
                    i += 1
                    if i == 89:
                        x_file.write('\n')
                        y_file.write('\n')
                        z_file.write('\n')
                        i = 0
            x_file.close()
            y_file.close()
            z_file.close()
        else:
            copy2(datafile_Path + '\\dataset_uci\\' + file, path + temp_file)
    else:
        copy2(datafile_Path + '\\dataset_uci\\' + file, new_datafile_path)
