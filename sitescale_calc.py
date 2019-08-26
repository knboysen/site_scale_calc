## This is an attempt at creating a python site scale calculator
## Kristen Boysen
## Updated 21 August 2019 

# Site Calculator Purpose: Using site-scale data, calculate habitat functionality
#-	Calculate Site Data Calculate Site-Scale Score 
#-	Using Modifiers, calculate habitat function for each season
#   Create output that can be visualized in GIS

## Data Clean and Import
    #Bring in Raw data
    #calculate percent cover from LPI 
    #from Survey 123 OR from excel/paper forms

#Calculate: 
    #Step 1: Import Data
        #input: data table (excel for now) 
            # 1 site, multiple map units, habitat variables as features
    #Step 2: For Forb Cover, Desirable Forb Cover, Shrub Cover, Desirable Shrub Cover, convert % covers into scores
    #Step 3: Combine scores using appropriate weights for each season.
        #output: input table with additional columns: habitat variable scores and roll-up scores for each season
        #save as excel 

#Integrate with HQT
    #For each season, multiply seasonal modifier to calculate habitat function. 
    #Output sexy map/print out

#Output: 
#Table with
#Habitat Functionality for each Season (Summer, Migration, Winter) 




import pandas as pd
import numpy as np
from collections import OrderedDict

#############################
#Step 1: Import Data

input_file = r'field_data_example.xlsx'
site_data = pd.read_excel(input_file)


#define if we are in majority PJ Habitat
#this should be a read-in from GIS) 


############
#Step 2. Convert Percent Covers into Scores
### Defining Scoring Curves
    #there must be a better way to do this-- can I read in an scoring table? 

## Instead we are trying to read in the scoring curves from a table

#Psuedo Code 
    # read in table!
    #   pct cover 0-100, score for each attribute
    #need value and column name to lookup where those two cross
    #return that value as the score
    #map funtion onto each column 

scores= pd.read_excel('field_scores.xlsx', index_col="pct_cover")

my_dict= OrderedDict([
    ('forb_score_s', 'forb_cover'),
    ('des_forb_score_s', 'des_forb_cov'),
    ('shrub_score_s', 'shrub_cover'),
    ('forb_score_m', 'forb_cover'),
    ('des_forb_score_m', 'des_forb_cov'),
    ('shrub_score_m', 'shrub_cover'),
    ('shrub_score_w', 'shrub_cover'),
    ('des_shrub_score_w', 'des_shrub_cover')
    ])

def score_match(hab_value, var_name):
    """
    Looks up a score from the 'scores' dataframe for the measure of any 
    habitat attribute (e.g., 35 percent cover of forb_cover). 
    :param hab_value: measure of the habitat attribute from 0 to 100
    :param var_name: name of the habitat attribute, must correspond to column
    name in site_data dataframe.
    """
    return scores.loc[round(hab_value), var_name]

for score, value in my_dict.items():
    site_data[score] = site_data.apply(lambda df:score_match(df[value], score), 
    axis =1)

########
#Add Weights
#Read in Table of Vegetation Weights
weights_df= pd.read_excel('site_calc_weights.xlsx')

#Convert to Dictionary
weight_dict = dict(zip(weights_df['veg_attribute'], weights_df['weight']))


def sum_func(shrub,forb, dforb):

    """
    Calculates summer habitat functionality score by multiplying vegetation attribute scores by their weight (as defined by weight_dict), and then adding across attributes. 
    :param shrub: shrub cover score, as per attribute scoring curves
    :param forb: forb cover score, as per attribute scoring curves
    :param dforb: desirable forb cover score, as per attribute scoring curves
    :return the combined summer score
    """

    s_score = shrub * weight_dict['sum_shrub_wt'] + forb *  weight_dict['sum_forb_wt']+ dforb *  weight_dict['sum_des_forb_wt']
    return s_score

def migration_func(shrub,forb, dforb):

    """
    Calculates migratory/transition habitat functionality score by multiplying vegetation attribute scores by their weight (as defined by weight_dict), and then adding across attributes. 
    :param shrub: shrub cover score, as per attribute scoring curves
    :param forb: forb cover score, as per attribute scoring curves
    :param dforb: desirable forb cover score, as per attribute scoring curves
    :return the combined migration habitat score
    """

    m_score = (shrub * weight_dict['mig_shrub_wt']) + (forb *  weight_dict['mig_forb_wt']) + (dforb * weight_dict['mig_des_forb_wt'])
    return m_score


def winter_func(shrub, dshrub):
    
    """
    Calculates winter habitat functionality score by multiplying vegetation attribute scores by their weight (as defined by weight_dict), and then adding across attributes. 
    :param shrub: shrub cover score, as per attribute scoring curves
    :param dshrub: desirable shrub cover score, as per attribute scoring curves
    :return the combined winter score
    """
    
    w_score= shrub * weight_dict['win_shrub_wt'] + dshrub * weight_dict['win_des_shrub_wt']
    return w_score

##add site functionality to data frame

site_data['s_func']= site_data.apply(lambda x:sum_func(x.shrub_cover_score, x.forb_cover_score, x.d_forb_score), axis= 1)

site_data['m_func']= site_data.apply(lambda x:migration_func(x.shrub_cover_score, x.forb_cover_score, x.d_forb_score), axis= 1)

site_data['w_func']= site_data.apply(lambda x:winter_func(x.winter_shrub_score, x.winter_d_shrub_score), axis= 1)

site_data['w_func_pj']= site_data.apply(lambda x:winter_func(x.winter_shrub_pj_score, x.winter_d_shrub_score), axis= 1)


site_data.to_excel("func_acres_output.xlsx")

## next steps
# integrate modifiers 
# call modifers from GIS? 


#######
## Other tasks!
    # How do we determine PJ/non PJ for winter habitat? 
    # what are the best practices for data cleaning? 