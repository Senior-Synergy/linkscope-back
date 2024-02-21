import numpy as np
feature_names = [ 'domainlength', 'www', 'subdomain', 
                 'https', 'http', 'short_url', 'ip', 
                 '@','-', '=','.', '_','/','digit', 
                 'log', 'pay', 'web', 'cmd', 'account',
                 'pcemptylinks', 'pcextlinks', 'pcrequrl',
                 'zerolink','extfavicon', 'submit2email',
                 'sfh', 'redirection', 'domainage', 'domainend']
num_features = [ 'domainlength',  '@', '-', '=', '.', '_', '/', 'digit',  'pcemptylinks', 'pcextlinks', 'pcrequrl']
cat_features = ['www', 'subdomain', 'https', 'http','short_url','ip','log', 'pay', 'web', 'cmd', 'account','zerolink', 'extfavicon',
       'submit2email','sfh','redirection', 'domainage', 'domainend']

def replace_minus_one(X):
    return X.replace(-1, np.nan)
def cast_to_float(X):
    return X.astype(float)
def cast_to_int(X):
    return X.astype(int)