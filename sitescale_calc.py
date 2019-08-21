## This is an attempt at creating a python site scale calculator
## Kristen Boysen
## Updated 21 August 2019 

# Site Calculator Purpose: Using site-scale data, calculate habitat functionality
#-	Calculate Site Data Calculate Site-Scale Score 
#-	Using Modifiers, calculate habitat function for each season
#   Create output that can be visualized in GIS

#Step 1: Import Data
#Step 2: For Forb Cover, Desirable Forb Cover, Shrub Cover, Desirable Shrub Cover, convert % covers into scores
#Step 3: Combine scores using appropriate weights for each season. 
#Step 4. For each season, multiply seasonal modifier to calculate habitat function. 

#Output: 
#Table with
#Habitat Functionality for each Season (Summer, Migration, Winter) 




import pandas as pd
import numpy as np

#############################
#Step 1: Import Data

site_data = r'field_data_example.xlsx'
sitedata = pd.read_excel(site_data)

scores= pd.read_excel('field_scores.xlsx')

#define if we are in majority PJ Habitat
#this should be a read-in from GIS) 


############
#Step 2. Convert Percent Covers into Scores
### Defining Scoring Curves
    #there must be a better way to do this-- can I read in an scoring table? 

### Migration/Summer Scoring Functions

# Forb Cover
def summerforb(perc): 
    if perc <= 30: 
        score = 0.05
    elif perc <= 60: 
        score = 0.33
    else: 
        score = 1
    return score

#Desirable Forb
def desirable_forb(perc):
    if perc <= 25: 
        score = .25
    elif perc <= 50: 
        score= .50
    elif perc <= 75:
        score = .75
    else: 
        score = 1
    return (score)

#Shrub Cover
def summershrub(perc): 
    if perc <= 15:
        score = 0.2
    elif perc <= 30: 
        score = 0.5
    elif perc <= 50: 
        score = 0.8
    elif perc <= 60:
        score = 1.0
    else: 
        score = 0.5
    return score

########## WINTER

#Shrub Cover in non PJ-- Winter
def wintershrub_nonpj(perc): 
    if perc <= 5:
        score = 0.0
    elif perc <= 20: 
        score = 0.5
    elif perc > 20: 
        score = 1.0
    return score

## Shrub Cover in PJ -- Winter
def wintershrub_pj(perc):
    if perc <= 5:
        score = 0.0
    elif perc <= 75: 
        score = 1.0
    elif perc <= 90:
        score = .1
    else: 
        score = 0
    return score

### Preferred Shrub--Winter
def winterpref_shrub(perc):
    if perc <= 25:
        score = .25
    elif perc <= 50: 
        score = .5
    elif perc <= 75: 
        score = .75
    else: 
        score = 1.0 
    return score

#Convert Percent Covers in Scores 

sitedata['forbcoverscore'] = sitedata['Forb Cover'].map(summerforb)

sitedata['dforbscore'] = sitedata['Des Forb Cover'].map(desirable_forb)

sitedata['shrubcoverscore'] = sitedata['Shrub Cover'].map(summershrub)

sitedata['wintershrubscore'] = sitedata['Shrub Cover'].map(wintershrub_nonpj)

sitedata['wintershrub_pjscore'] = sitedata['Shrub Cover'].map(wintershrub_pj)

sitedata['wintershrub_prefscore'] = sitedata['Preferred Shrub Cover'].map(winterpref_shrub)

##################
### combine data

##Summer/Migration Score
def sum_migration_func(shrub,forb, dforb):
    s_m_score = shrub*.5 + forb*.25 + dforb*.25
    return s_m_score

def w_func(shrub, dshrub):
    w_score= shrub *.50 + dshrub *.50
    return w_score

##add site functionality to data frame
sitedata['s_func']= sitedata.apply(lambda x:sum_migration_func(x.shrubcoverscore, x.forbcoverscore, x.dforbscore), axis= 1)

sitedata['w_func']= sitedata.apply(lambda x:w_func(x.wintershrubscore, x.wintershrub_prefscore), axis= 1)

sitedata['w_func_pj']= sitedata.apply(lambda x:w_func(x.wintershrub_pjscore, x.wintershrub_prefscore), axis= 1)


#sitedata.to_excel("func_acres_output.xlsx")

## next steps
# integrate modifiers 
# call modifers from GIS? 


#######
## Other tasks!
    # How do we determine PJ/non PJ for winter habitat? 
    # what are the best practices for data cleaning? 