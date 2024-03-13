from testloadmodel import *

model = load_model("data/model_new.gzip") 
url = '9418265.fls.doubleclick.net'
obj = URLresult(url, model)
print(obj.get_final_url())
print(obj.get_phish_prob())
print(obj.get_isPhish())
#file.close()