import glob
import pandas as pd

class Data_Reader:
    def __init__(self, lake_names):
        self.lake_names = lake_names
        self.data_rel_path = "./processed_data/"
    
    def __construct_raw_df(self, lake):
        '''
        private helper function to construct raw data frame
        for each lake

        returns a pandas data frame
        '''
        # variables to accumulate the lake data
        rep_numbers = []
        rep_names = []
        wavelengths = []
        asd_measures = []

        lake_data_path = self.data_rel_path + lake + '/'
        lake_data_file_paths = sorted(
            glob.glob(lake_data_path + lake + '*asd.txt'))
        for path in lake_data_file_paths:
            data_file_name = path.split("/")[3]
            rep_number = int(data_file_name.split("_")[1])
            rep_ext = data_file_name.split("_")[2]
            rep_name = rep_ext.split("0")[0]
            file_data = pd.read_csv(path, sep="\t")
            file_data.columns = ["wavelength", "asd_measure"]
            for row in file_data.iterrows():
                row_data = row[1]
                rep_numbers.append(rep_number)
                rep_names.append(rep_name)
                wavelengths.append(row_data["wavelength"])
                asd_measures.append(row_data["asd_measure"])

        lake_data = {}
        lake_data["rep_number"] = rep_numbers
        lake_data["rep_name"] = rep_names
        lake_data["wavelength"] = wavelengths
        lake_data["asd_measure"] = asd_measures
        return pd.DataFrame.from_dict(lake_data)
    
    def get_raw_data(self):
        '''
        returns a list of raw data frames for each lake 
        '''
        result = []
        for lake in self.lake_names:
            lake_df = self.__construct_raw_df(lake)
            # get the mean of 3-5 reps
            mean_by_rep_type = lake_df.groupby(
                ["rep_number", "rep_name", "wavelength"]).mean()
            mean_by_rep_type = mean_by_rep_type.reset_index()
            result.append(mean_by_rep_type)
        return result
