import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def load_data():
  ''' For loading data in each sheet to DataFrames

  Returns : DataFrames with data of each subject
  
  '''
  maths_df = pd.read_excel('Python_Assignment.xlsx', sheet_name= 'Maths')
  phy_df = pd.read_excel('Python_Assignment.xlsx', sheet_name= 'Physics')
  hindi_df = pd.read_excel('Python_Assignment.xlsx', sheet_name= 'Hindi')
  eco_df = pd.read_excel('Python_Assignment.xlsx', sheet_name= 'Economics')
  music_df = pd.read_excel('Python_Assignment.xlsx', sheet_name= 'Music')

  return maths_df, phy_df, hindi_df, eco_df, music_df

def percent_cal(maths_df, phy_df, hindi_df, eco_df, music_df):
  ''' For calculating percentage of each subject

  Input   : Maths DataFrame, Physics DataFrame, Hindi DataFrame, Economics DataFrame, Music DataFrame
  Returns : All subjects DataFrames with columns 'Roll No','Class','<subject percentage>'
  
  '''
  maths_df['maths'] =round(((maths_df['Theory Marks'] + maths_df['Numerical Marks'] + maths_df['Practical Marks'])/300)* 100,2)
  phy_df['Physics'] =round(((phy_df['Theory Marks'] + phy_df['Numerical Marks'] + phy_df['Practical Marks'])/300)* 100,2)
  hindi_df['Hindi'] =round((hindi_df['Marks']/100)* 100,2)
  eco_df['Economics'] =round(((eco_df['Theory Marks'] + eco_df['Numerical Marks'])/200)* 100,2)
  music_df['Music'] =round(((music_df['Theory Marks'] + music_df['Practical Marks'])/200)* 100,2)
  maths_df_per = maths_df.loc[:, ['Roll No','Class','maths']]
  phy_df_per = phy_df.loc[:, ['Roll No','Class','Physics']]
  hindi_df_per = hindi_df.loc[:, ['Roll No','Class','Hindi']]
  eco_df_per = eco_df.loc[:, ['Roll No','Class','Economics']]
  music_df_per = music_df.loc[:, ['Roll No','Class','Music']]
  
  return maths_df_per, phy_df_per, hindi_df_per, eco_df_per, music_df_per

def merger(maths_df_per, phy_df_per, hindi_df_per, eco_df_per, music_df_per):
  ''' For merging all subjects DataFrames
  
  Input : All subjects DataFrames with columns 'Roll No','Class','<subject percentage>'
  Returns : Merged DataFrame

  '''
  result = maths_df_per.merge(phy_df_per, on = ['Class', 'Roll No'], how = 'outer').merge(hindi_df_per, on = ['Class', 'Roll No'], how = 'outer').merge(eco_df_per, on = ['Class', 'Roll No'], how = 'outer').merge(music_df_per, on = ['Class', 'Roll No'], how = 'outer')
  return result

def most_nums(merged_df):
  ''' To calculate Which class has the most number of students?

  Input : Merged DataFrame
  Returns : Which class has the most number of students?

  '''
  most_num = pd.DataFrame(columns = ['Class','Students'])
  most_num['Class'] = merged_df['Class'].value_counts()[:5].index
  lists = merged_df['Class'].value_counts()[:5].to_list()
  most_num['Students'] = lists
  return most_num

def class_mean(merged_df):
  ''' To calculate Which class has the highest average percentage of marks across all subjects?

  Input : Merged DataFrame
  Returns : Which class has the highest average percentage of marks across all subjects?

  '''
  mean_df = pd.DataFrame(merged_df.groupby(['Class'], as_index=False)['maths','Physics','Hindi', 'Economics','Music'].mean())
  mean_df['class_mean'] = np.sum(mean_df, axis = 1)
  result = int(mean_df.loc[mean_df['class_mean'] == mean_df['class_mean'].max()].iloc[0][0])
  return result

def subs_mean(merged_df):
  ''' To calculate Which subject has the highest average percentage of marks across all classes?

  Input : Merged DataFrame
  Returns : Which subject has the highest average percentage of marks across all classes?

  '''
  mean_df = pd.DataFrame(merged_df.groupby(['Class'], as_index=False)['maths','Physics','Hindi', 'Economics','Music'].mean().T)
  mean_df = mean_df.iloc[1: , :]
  mean_df['subjects_mean'] = np.sum(mean_df, axis = 1)
  result = mean_df.loc[mean_df['subjects_mean'] == mean_df['subjects_mean'].max()].index.to_list()[0]
  return result

if __name__ =="__main__":
  
  maths_df, phy_df, hindi_df, eco_df, music_df = load_data()
  maths_df_per, phy_df_per, hindi_df_per, eco_df_per, music_df_per = percent_cal(maths_df, phy_df, hindi_df, eco_df, music_df)
  merged_df = merger(maths_df_per, phy_df_per, hindi_df_per, eco_df_per, music_df_per)

  print('How many students in total are enrolled with the tuition provider?\n', merged_df.shape[0])
  print('\nHow many students have taken all the five subjects?\n',merged_df.dropna().shape[0])
  print('\nWhich class has the most number of students?\n',most_nums(merged_df))
  print('\nWhich class has the highest average percentage of marks across all subjects?\n', class_mean(merged_df))
  print('\nWhich subject has the highest average percentage of marks across all classes?\n', subs_mean(merged_df))

