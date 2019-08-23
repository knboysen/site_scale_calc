### dictionary practice
 

##define dictionary

post= {
    "user": 209, 
    "message": "hihihi", 
    "lang": "English", 
    "loc": "DEN"
}
 
 post2= dict(user= 210, lang= "Spanish")
 post2["loc"]= "MEX"

 for key in post.keys():
     value= post[key]
     print(key, "=", value)


for key, value in post.items():
    print(key, "=", value)

from pandas import DataFrame

df = DataFrame([['A', 123, 1], ['B', 345, 5], ['C', 712, 4], ['B', 768, 2], ['A', 318, 9], ['C', 178, 6], ['A', 321, 3]], columns=['name', 'value1', 'value2'])

d = {}
for i in df['name'].unique():
    d[i] = [{df['value1'][j]: df['value2'][j]} for j in df[df['name']==i].index]



weights= pd.read_excel('site_calc_weights.xlsx')

for i in weights():
    weights["veg_attribute"]= weights["weight"]

# weight_dict = weights.to_dict('series')

# x = {}
# for i in weights['veg_attribute'].unique:
#     x[i] = weights['weight']

#  for key in weight_dict.keys():
#      value= weight_dict[key]
#      print(key, "=", value)


for row in weights.itertuples():
    x = weights['veg_attribute']
    veg_attribute 