import os
import pandas as pd
import matplotlib.pylab as plt

## Function to get individual plot ids based on categories in original metadata file
## WILL NOT WORK if you have a different filename for metadata
## Takes one or more strings that are possible variables to id samples with
## Returns list of sample ids that fit those criteria
## USE: for getting the names of samples you want to remove or subset
def get_id(*args):
	list_of_req = [x for x in args]
	parent_directory = os.path.abspath('..')
	metadata_original = pd.read_csv(parent_directory+'/Metadata/project_metadata_original.csv', dtype={'Date': object, 'Rep':object}, skiprows=0, delimiter= '\t')
	metadata_original_dict = metadata_original.to_dict('list')
	metadata_original_dict_set = {}
	for i in metadata_original_dict:
		if i == 'ID':
			continue
		else:
			metadata_original_dict_set[i] = [str(k) for k in set(metadata_original_dict[i])]
	metadata_original_subset = metadata_original
	total_count = 0
	for m in list_of_req:
		count = 0
		for j in metadata_original_dict_set:
			if m in metadata_original_dict_set[j]:
				count += 1
				total_count += 1
				print j, m
				metadata_original_subset = metadata_original_subset.loc[(metadata_original_subset[j] == m)]
        if count == 0:
            if len(list_of_req) > 1:
                print 'ERROR: Value',m,'not a possible value. Subsetting by other values.'
            else:
				print 'ERROR: Value',m,'not a possible value.'
	if total_count > 0:
		return [i for i in metadata_original_subset['ID']]
	else:
		return 'ERROR: None of the entered arguments match possible values in the metadata file.'

## Plotting multiple dataframes or csv 
def plotting_multiple_files(dict_of_files, title='Title', check='F'):
	linestyles = {'fil':'--','raw':'-','vic':'-'}
	for reps in sorted(list(dict_of_files)):
		Sample_Type = reps.split(' ')[0]
		if not isinstance(dict_of_files[reps], pd.DataFrame):
			df = pd.read_csv(dict_of_files[reps], skiprows = 0, delimiter= '\t')
		else:
			df = dict_of_files[reps]
		df.reset_index(inplace=True, drop=False)
		df.rename(columns = {'c_mean':'mean', 'a_mean':'mean', 'c_std':'std','a_std':'std'}, inplace = True)
		plt.plot('wl','mean',data=df,label=reps,linestyle=linestyles[Sample_Type])
		plt.errorbar('wl', 'mean', yerr='std', fmt='k-', linewidth=0.5, data = df) 
	plt.ylabel('[1/m]')
	plt.xlabel('Wavelength (nm)')
	plt.title(title)
	plt.legend(sorted(list(dict_of_files)))
	return plt

def make_dir(mystring, show='FALSE'):
    import os
    def getpath(mystring2):
        if not os.path.exists(mystring2):
            os.makedirs(mystring2)
    if os.getcwd().split('/')[-1] != 'Code':
        print 'Error: Current working directory should be the "Code" subdirectory of the current project.'
    else:
        if '..' in mystring:
            if show == 'TRUE':
                print 'Created directory: '+mystring
            getpath(mystring)
        else:
            parent_directory = os.path.abspath('..')
            newname = parent_directory+'/'+mystring
            if show == 'TRUE':
                print 'Created directory: '+newname
            getpath(newname)
            return newname