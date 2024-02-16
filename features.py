
from urllib.parse import urlparse
from tld import get_tld, is_tld
import tldextract
import whois
import datetime
from datetime import datetime
import time
from bs4 import BeautifulSoup
import re

import requests
headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

class FeatureExtraction:
    features = []
    def __init__(self,urlt):
        self.features = []
        urldata = self.getfinalurl(urlt)
        self.url = urldata[0]
        self.soup = urldata[1]
        self.urlhistory = urldata[2]
        print("get soup successfully")

        try:
            self.domain_name = whois.whois(urlparse(url).netloc)
        except Exception:
            self.domain_name = None
        print("get whois successfully")
        
        # self.features.append(urlt)
        # Address bar based features (10)
        self.features.append(self.getdomainlength()) #1
        self.features.append(self.contains_www())  #2 
        self.features.append(self.has_subdomain()) #3
        self.features.append(self.httpSecure()) #4
        self.features.append(self.http()) #5
        self.features.append(self.short_url()) #6
        self.features.append(self.having_ip_address()) #7
                
        self.features.append(self.count_at_symbols()) #8
        self.features.append(self.count_dash_symbols()) #9   
        self.features.append(self.count_equal_symbols()) #10
        self.features.append(self.count_dot_symbols()) #11
        self.features.append(self.count_underscore_symbols()) #12
        self.features.append(self.count_slash_symbols()) #13
        self.features.append(self.digit_count()) #14
        
        self.features.append(self.contains_log()) #15
        self.features.append(self.contains_pay()) #16
        self.features.append(self.contains_web()) #17
        self.features.append(self.contains_cmd()) #18
        self.features.append(self.contains_account()) #19
        
        # HTML and Javascript based features
        self.features.append(self.calpc_emptylinks()) #20
        self.features.append(self.calpc_extlinks()) #21
        self.features.append(self.calpc_requrl()) #22
        self.features.append(self.haszerolinksinbody()) #23
        self.features.append(self.has_external_favicon()) #24
        self.features.append(self.submit2Email()) #25
        self.features.append(self.sfh()) #26
        self.features.append(self.redirection()) #27
        
        #Domain based features
        self.features.append(self.domainAge() if self.domain_name else -1) #28
        self.features.append(self.domainEnd() if self.domain_name else -1 ) #29
        
    # 0.UsingIp
    def getfinalurl(self):
        parsed_url = urlparse(self.url)
        final_url = self.url
        soup = None
        urlhistory = None
        if not parsed_url.scheme:
            final_url = "http://" + self.url
        try:
            response = requests.get(final_url, allow_redirects=True, headers={'User-Agent': headers}, timeout = 2) #  ,allow_redirects=True
            final_url = response.url
            soup = BeautifulSoup(response.text, 'html.parser')
            urlhistory = response.history
            return final_url, soup, urlhistory
        except requests.RequestException:
            return final_url, soup, urlhistory
        except Exception:
            return final_url, soup, urlhistory

    # 1 Get hostname length
    def getdomainlength(self):
        hostname = urlparse(self.url).hostname
        if hostname:
            domain_length = len(hostname)
            return domain_length
        return -1

    # 2 Whether it contains www 
    def contains_www(self):
        hostname = urlparse(self.url).hostname
        if hostname:
            if "www" in hostname[0:3]:
                return 0
            else:
                return 1
        return -1

    # 3 has subdomain or not
    def has_subdomain(self):
        ext = tldextract.extract(self.url)
        subd = ext.subdomain
        subd_parts = subd.split('.')
        if subd_parts:
            if len(subd_parts) > 1:
                return 1
            else:
                return 0
        return -1
    
    # 4 checks https
    def httpSecure(self):
        htp = urlparse(self.url).scheme
        match = str(htp) 
        if htp:
            if match == 'https':
                return 0 
            else:
                return 1
        return -1
    
    # 5 check http
    def http(self):
        htp = urlparse(self.url).scheme
        match = str(htp)
        if htp:
            if match == 'https' or match == 'http':
                return 0 
            else:
                return 1
        return -1
    
    # 6 short url : tested
    def short_url(self):
        pattern = 'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|' \
            'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|' \
            'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|' \
            'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|' \
            'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|' \
            'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|' \
            'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|' \
            'tr\.im|link\.zip\.net'
        match = re.search(pattern, self.url)
        if match:
            return 1
        else:
            return 0

    # 7 Use the IP Address : tested
    def having_ip_address(self):
        match = re.search(
            '(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
            '([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)' # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', self.url)  # Ipv6
        if match:
            return 1
        else:
            return 0
        
    # 8
    def count_at_symbols(self):
        return self.url.count("@")

    # 9
    def count_dash_symbols(self):
        return self.url.count("-")

    # 10
    def count_equal_symbols(self):
        return self.url.count("=")

    # 11
    def count_dot_symbols(self):
        hostname = urlparse(self.url).hostname
        if hostname:
            return hostname.count(".")
        return  -1

    # 12 
    def count_underscore_symbols(self):
        return self.url.count("_")

    # 13
    def count_slash_symbols(self):
        return self.url.count("/")
    
    # 14 count digit : tested
    def digit_count(self):
        hostname = urlparse(self.url).hostname
        digits = 0
        if hostname:
            for i in hostname:
                if i.isnumeric():
                    digits = digits + 1
            return digits
        else:
            return -1
        
    # 15 if contain keyword => 1 (phish), else => 0 (safe)
    def contains_log(self):
        if 'log' in self.url.lower():
            return 1
        return 0
    # 16
    def contains_pay(self):
        if 'pay' in self.url.lower():
            return 1
        return 0
    # 17
    def contains_web(self):
        if 'web' in self.url.lower():
            return 1
        return 0
    # 18
    def contains_cmd(self):
        if 'cmd' in self.url.lower():
            return 1
        return 0
    # 19
    def contains_account(self):
        if 'account' in self.url.lower():
            return 1
        return 0
        
    # 20 Percentage of links that do not lead to another page
    def calpc_emptylinks(self):
        try:
            all_links = self.soup.find_all('a', href=True)
            total_links_count = len(all_links)
            empty_links_count = 0
            for link in all_links:
                if '#' == link['href'][0] or link['href'] == '' or "javascript:void(0)" in link['href'] or "./" == link['href'] :
                    empty_links_count += 1
            if total_links_count > 0 :
                percentage_empty_links = (empty_links_count / total_links_count) * 100  
            else:
                percentage_empty_links = 0
            return percentage_empty_links
        except:
            return -1

    # 21 Percentage of links that lead to an external page.
    def calpc_extlinks(self):
        try:
            all_links = self.soup.find_all('a', href=True)
            total_links_count = len(all_links)
            page_domain = tldextract.extract(self.url).domain
            external_links_count = 0
            for link in all_links:
                if link['href'].split(":")[0] in ['http','https'] and not page_domain in link['href']:
                    external_links_count += 1
            if total_links_count > 0 :
                percentage_external_links = (external_links_count / total_links_count) * 100  
            else:
                percentage_external_links = 0

            return percentage_external_links
        except Exception:
            return -1

    # 22 Percentage of external resources URL /Request URL ,examines whether the external objects contained within a webpage
    def calpc_requrl(self):
        i = 0
        success = 0
        try:
            page_domain = tldextract.extract(self.url).domain
            for img in self.soup.find_all('img', src=True):
                if img['src'].split(":")[0] in ['http','https'] and not page_domain in img['src']:
                    success += 1
                i += 1
            for audio in self.soup.find_all('audio', src=True):
                if audio['src'].split(":")[0] in ['http','https'] and not page_domain in audio['src']:
                    success += 1
                i += 1
            for embed in self.soup.find_all('embed', src=True):
                if embed['src'].split(":")[0] in ['http','https'] and not page_domain in embed['src']:
                    success += 1
                i += 1
            for iframe in self.soup.find_all('iframe', src=True):
                if iframe['src'].split(":")[0] in ['http','https'] and not page_domain in iframe['src']:
                    success += 1
                i += 1
            if i > 0:
                percentage = (success/float(i) * 100)
            else:
                percentage = 0
            return percentage
        except Exception:
            return -1

    # 23 Zero links in body portion of HTML
    def haszerolinksinbody(self):
        try:
            body_links = self.soup.body.find_all('a', href=True)
            if len(body_links) == 0:
                return 1
            return 0
        except Exception:
            return -1

    # 24 external favicon
    def has_external_favicon(self):
        try:
            favicon_links = self.soup.find_all('link', rel=['icon', 'shortcut icon'])
            page_domain = tldextract.extract(self.url).domain
            external_favicon_count = 0
            for favicon_link in favicon_links:
                if favicon_link['href'].split(":")[0] in ['http', 'https'] and not page_domain in favicon_link['href']:
                    external_favicon_count += 1
            if external_favicon_count == 0:
                return 0
            else:
                return 1
        except Exception:
            return -1
        
    # 25 submit2Email
    def submit2Email(self):
        try:
            if re.search(r"\b(mail\(\)|mailto:?)\b", self.soup.text, re.IGNORECASE):
                return 1
            else:
                return 0
        except Exception:
            return -1
        
    # 26 SFHs that contain an empty string or “about:blank” are considered doubtful
    def sfh(self):
        try:
            domain = tldextract.extract(self.url).domain
            for form in self.soup.find_all('form', action=True):
                if form['action'] == "" or form['action'] == "about:blank":
                    return 1
                elif self.url not in form['action'] and domain not in form['action']:
                    return 1
                else:
                    return 0
            return 0
        except Exception:
            return -1
    
    # 27 redirection
    def redirection(self):
        try:
            if len(self.urlhistory) > 1:
                return 1
            else:
                return 0
        except Exception:
            return -1

    # 28 Domain Age : Survival time of domain: The difference between termination time and creation time (Domain_Age)  
    def domainAge(self):
        creation_date = self.domain.creation_date
        expiration_date = self.domain.expiration_date
        ageofdomain = 0
        if (expiration_date is None) or (creation_date is None):
            return 1
        elif type(expiration_date) is list:
            expiration_date = self.domain.expiration_date[0]
        elif type(creation_date) is list:
            creation_date = self.domain.creation_date[0]
        elif type(creation_date) is str or type(expiration_date) is str:
            return -1
        else:
            ageofdomain = abs((expiration_date - creation_date).days)
        return 1 if (ageofdomain/30) < 6 else 0

    # 29 Domain Registration length
    def domainEnd(self):
        expiration_date = self.domain.expiration_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = 0
        if expiration_date is None:
            return 1
        elif type(expiration_date) is list:
            expiration_date = self.domain.expiration_date[0]
        elif type(expiration_date) is str:
            return -1
        else:
            registration_length = abs((expiration_date - today).days)
        return 1 if registration_length / 365 <= 1 else 0
    
    def getFeaturesList(self):
        return self.features