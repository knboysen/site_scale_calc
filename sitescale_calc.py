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
    round_hab_value = round(hab_value) #rounds to nearest integer
    row = scores.loc[round_hab_value]
    return row[var_name]

for score, value in my_dict.items():
    site_data[score] = site_data.apply(lambda x:score_match(x[value], score), 
    axis =1)




#site_data['forb_cover_score']= site_data.apply(lambda x:score_match(x.forb_cover, "forb_score"), axis= 1)

### Migration/Summer Scoring Functions

# # Forb Cover
# def summerforb(perc): 
#     if perc <= 30: 
#         score = 0.05
#     elif perc <= 60: 
#         score = 0.33
#     else: 
#         score = 1
#     return score

# #Desirable Forb
# def desirable_forb(perc):
#     if perc <= 25: 
#         score = .25
#     elif perc <= 50: 
#         score= .50
#     elif perc <= 75:
#         score = .75
#     else: 
#         score = 1
#     return (score)

# #Shrub Cover
# def summershrub(perc): 
#     if perc <= 15:
#         score = 0.2
#     elif perc <= 30: 
#         score = 0.5
#     elif perc <= 50: 
#         score = 0.8
#     elif perc <= 60:
#         score = 1.0
#     else: 
#         score = 0.5
#     return score

# ########## WINTER

# #Shrub Cover in non PJ-- Winter
# def wintershrub_nonpj(perc): 
#     if perc <= 5:
#         score = 0.0
#     elif perc <= 20: 
#         score = 0.5
#     elif perc > 20: 
#         score = 1.0
#     return score

# ## Shrub Cover in PJ -- Winter
# def wintershrub_pj(perc):
#     """This function takes percent cover of all shrubs in PJ and outputs score based on scoring curves in Mule Deer Methods Doc"""
#     if perc <= 5:
#         score = 0.0
#     elif perc <= 75: 
#         score = 1.0
#     elif perc <= 90:
#         score = .1
#     else: 
#         score = 0
#     return score

# ### Preferred Shrub--Winter
# def winterpref_shrub(perc):
#     if perc <= 25:
#         score = .25
#     elif perc <= 50: 
#         score = .5
#     elif perc <= 75: 
#         score = .75
#     else: 
#         score = 1.0 
#     return score

#Convert Percent Covers in Scores 

# site_data['forb_cover_score'] = site_data['forb_cover'].map(summerforb)

# site_data['d_forb_score'] = site_data['des_forb_cov'].map(desirable_forb)

# site_data['shrub_cover_score'] = site_data['shrub_cover'].map(summershrub)

# site_data['winter_shrub_score'] = site_data['shrub_cover'].map(wintershrub_nonpj)

# site_data['winter_shrub_pj_score'] = site_data['shrub_cover'].map(wintershrub_pj)

# site_data['winter_d_shrub_score'] = site_data['des_shrub_cover'].map(winterpref_shrub)

##################
### combine data

##Summer/Migration Score
def sum_migration_func(shrub,forb, dforb):
    s_m_score = shrub * 0.5 + forb * 0.25 + dforb * 0.25
    return s_m_score

def w_func(shrub, dshrub):
    w_score= shrub * 0.50 + dshrub * 0.50
    return w_score

##add site functionality to data frame
site_data['s_func']= site_data.apply(lambda x:sum_migration_func(x.shrub_cover_score, x.forb_cover_score, x.d_forb_score), axis= 1)

site_data['m_func']= site_data.apply(lambda x:sum_migration_func(x.shrub_cover_score, x.forb_cover_score, x.d_forb_score), axis= 1)

site_data['w_func']= site_data.apply(lambda x:w_func(x.winter_shrub_score, x.winter_d_shrub_score), axis= 1)

site_data['w_func_pj']= site_data.apply(lambda x:w_func(x.winter_shrub_pj_score, x.winter_d_shrub_score), axis= 1)


site_data.to_excel("func_acres_output.xlsx")

## next steps
# integrate modifiers 
# call modifers from GIS? 


#######
## Other tasks!
    # How do we determine PJ/non PJ for winter habitat? 
    # what are the best practices for data cleaning? 