from testloadmodel import *

model = load_model("data/model_compressed.gzip") 
url = '9418265.fls.doubleclick.net'
obj = URLresult(url, model)
print(obj.get_final_url())
print(obj.get_phish_prob())
print(obj.get_isPhish())
extracted_df = obj.features_df
features_arr = obj.features_arr
features_list = extracted_df.to_dict(orient='records')
print(features_list)
print(features_arr)

#file.close()