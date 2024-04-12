from testloadmodel import *
import json
from pandas import json_normalize
model = load_model("data/model_compressed.gzip") 
url = 'https://jujutsu-kaisen.fandom.com/wiki/Jujutsu_Kaisen_Wiki'
obj = URLresult(url, model)

extracted_df = obj.features_df
features_arr = obj.features_arr
final_url = obj.url
extra_features = obj.get_extra_features()
whois_features = dict(obj.get_whois_features())

print(extra_features)
print(whois_features)

#features_list = extracted_df.to_dict(orient='records')
#print(features_list)

#print(features_arr)
#file.close()
