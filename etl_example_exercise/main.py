import os
import pandas as pd

class ETL:

    def __init__(self):
        # Class Variable for input Folder
        self.__input_folders = ['Input/data_source_1', 'Input/data_source_2']

    def get_consolidated_data(self):
        """
        Read the data from all the input files
        return: Consolidated data from all input files
        """
        consolidated_data = pd.DataFrame()
        # Iterating through the input folders to get the files
        for folder in self.__input_folders:
            # List of files in each folder
            files_list = os.listdir(folder)
            # Iterating through each file in the input folders
            for files in files_list:
                # Read the file based on the file extension .csv|.dat
                if files.endswith(".csv"):
                    data_from_file = pd.read_csv('{}/{}'.format(folder, files), sep=',')
                elif files.endswith(".dat"):
                    f = open('{}/{}'.format(folder, files)).readlines()[0]
                    if '|' in f:
                        separator = '|'
                    elif ',' in f:
                        separator = ','
                    data_from_file = pd.read_csv('{}/{}'.format(folder, files), sep=separator)
                # Skip the file if the extension of the file doesn't match with .csv|.dat
                else:
                    continue
                # Adding the datasource(Foldername) to the retrieved dataframe
                data_from_file['datasource'] = folder.split('/')[1]
                # Add the data
                consolidated_data = pd.concat([consolidated_data, data_from_file])
        return consolidated_data

    def write_to_output_file(self, consolidated_data):
        """
        Write the consolidated data to the output folder
        :param consolidated_data: Consolidated data from all the input files
        """
        # Create the Output directort if not available
        if not os.path.isdir('Output'):
            os.mkdir('Output')
        # Write the data to the file
        consolidated_data.to_csv(r'Output/consolidated_output.1.csv', header=True) 


if __name__ == "__main__":
    obj = ETL()
    consolidated_data = obj.get_consolidated_data()
    obj.write_to_output_file(consolidated_data)
