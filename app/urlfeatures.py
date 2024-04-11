from urllib.parse import urlparse
from bs4 import BeautifulSoup
import tldextract
import whois
import datetime
from datetime import datetime
import time
import re
import requests
import json


headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


class URLFeatures:
    # features = []
    def __init__(self, urlt):

        urldata = self.getfinalurl(urlt)
        self.url = urldata[0]
        self.soup = urldata[1]
        self.urlhistory = urldata[2]

        self.hostname = self.get_hostname()  # or domain name
        self.domain = self.get_domain()
        self.subdomains = self.get_subdomain()
        self.scheme = self.get_scheme()
        self.shortten_url = self.get_shorturl()
        self.ip_in_url = self.get_ip_in_url()

        # all links
        self.all_links = self.get_all_links()
        # count all links
        self.len_all_links = len(self.all_links)

        # count empty link
        self.len_empty_links = self.count_empty_links()

        # external links
        self.external_links = self.get_external_links()
        # count external links
        self.len_external_links = len(self.external_links)

        # all img, audio, embed, iframe requrl
        self.img_requrl = self.get_img_requrl()
        self.audio_requrl = self.get_audio_requrl()
        self.embed_requrl = self.get_embed_img_requrl()
        self.iframe_requrl = self.get_iframe_requrl()
        # count all img, audio, embed, iframe requrl
        self.len_img_requrl = len(self.img_requrl)
        self.len_audio_requrl = len(self.audio_requrl)
        self.len_embed_requrl = len(self.embed_requrl)
        self.len_iframe_requrl = len(self.iframe_requrl)
        self.len_all_requrl = self.len_img_requrl + self.len_audio_requrl + \
            self.len_embed_requrl + self.len_iframe_requrl

        # external requrl
        self.external_img_requrl = self.get_external_img_requrl()
        self.external_audio_requrl = self.get_external_audio_requrl()
        self.external_embed_requrl = self.get_external_embed_requrl()
        self.external_iframe_requrl = self.get_external_iframe_requrl()
        # count all external img, audio, embed, iframe requrl
        self.len_external_img_requrl = len(self.external_img_requrl)
        self.len_external_audio_requrl = len(self.external_audio_requrl)
        self.len_external_embed_requrl = len(self.external_embed_requrl)
        self.len_external_iframe_requrl = len(self.external_iframe_requrl)
        self.len_all_external_requrl = self.len_external_img_requrl + self.len_external_audio_requrl + \
            self.len_external_embed_requrl + self.len_external_iframe_requrl
        # external favicon
        self.external_favicon = self.get_external_favicon()
        # count external favicon
        self.len_external_favicon = len(self.external_favicon)

        try:
            self.w = whois.whois(self.hostname)
        except Exception as e:
            print(f"Error calling whois {e}")
            self.w = None

        # if self.w:
            # domain creation date
        self.creation_date = self.get_creation_date()
        # domain expiration date
        self.expiration_date = self.get_expiration_date()

        # Age of domain
        self.domain_age = self.get_domainage()
        # Registration length of domain
        self.domain_end = self.get_domainend()

       # ------------- Data Dictionary---------------------------------
        self.features = {
            'domainlength': self.getdomainlength(),
            'www': self.contains_www(),
            'subdomain': self.has_subdomain(),  # 3
            'https': self.httpSecure(),  # 4
            'http': self.http(),  # 5
            'short_url': self.short_url(),  # 6
            'ip': self.having_ip_address(),  # 7
            'at_count': self.count_at_symbols(),  # 8
            'dash_count': self.count_dash_symbols(),  # 9
            'equal_count': self.count_equal_symbols(),  # 10
            'dot_count': self.count_dot_symbols(),  # 11
            'underscore_count': self.count_underscore_symbols(),  # 12
            'slash_count': self.count_slash_symbols(),  # 13
            'digit_count': self.digit_count(),  # 14
            'log_contain': self.contains_log(),  # 15
            'pay_contain': self.contains_pay(),  # 16
            'web_contain': self.contains_web(),  # 17
            'cmd_contain': self.contains_cmd(),  # 18
            'account_contain': self.contains_account(),  # 19
            'pc_emptylink': self.calpc_emptylinks(),  # 20
            'pc_extlink': self.calpc_extlinks(),  # 21
            'pc_requrl': self.calpc_requrl(),  # 22
            'zerolink': self.haszerolinksinbody(),  # 23
            'ext_favicon': self.has_external_favicon(),  # 24
            'submit_to_email': self.submit2Email(),  # 25
            'sfh':  self.sfh(),  # 26
            'redirection': self.redirection(),  # 27
            'domainage': self.domainAge() if self.w else -1,  # 28
            'domainend': self.domainEnd() if self.w else -1,
            # extra url info
            'shortten_url': self.shortten_url,
            'ip_in_url': self.ip_in_url,
            'len_empty_links': self.len_empty_links,

            'external_links': json.dumps(self.external_links) if self.soup and self.len_external_links != 0 else None,
            'len_external_links': self.len_external_links,

            'external_img_requrl': json.dumps(self.external_img_requrl) if self.len_external_img_requrl != 0 else None,
            'external_audio_requrl': json.dumps(self.external_audio_requrl) if self.len_external_audio_requrl != 0 else None,
            'external_embed_requrl': json.dumps(self.external_embed_requrl) if self.len_external_embed_requrl != 0 else None,
            'external_iframe_requrl': json.dumps(self.external_iframe_requrl) if self.len_external_iframe_requrl != 0 else None,

            'len_external_img_requrl': self.len_external_img_requrl,
            'len_external_audio_requrl': self.len_external_audio_requrl,
            'len_external_embed_requrl': self.len_external_embed_requrl,
            'len_external_iframe_requrl': self.len_external_iframe_requrl,
        }
        self.extra_info = {
            # extra url info
            'hostname': self.hostname,
            'domain': self.domain,
            'subdomains': None if self.has_subdomain() == 0 else json.dumps(self.subdomains),
            'scheme': self.scheme,
            # extra domain infomation
            'creation_date': self.creation_date if self.w else None,
            'expiration_date': self.expiration_date if self.w else None,
            'domainage': self.domain_age if self.w else None,
            'domainend': self.domain_end if self.w else None,
            'city': None if self.w is None or self.w.city is None or any(city in ['REDACTED FOR PRIVACY', 'DATA REDACTED'] for city in self.w.city) else self.w.city,
            'state': None if self.w is None or self.w.state is None or any(state in ['REDACTED FOR PRIVACY', 'DATA REDACTED'] for state in self.w.state) else self.w.state,
            'country': None if self.w is None or self.w.country is None or any(country in ['REDACTED FOR PRIVACY', 'DATA REDACTED'] for country in self.w.country) else self.w.country
        }

    def get_model_features(self):
        return self.features

    def get_extra_info(self):
        return self.extra_info

    # 0.UsingIp
    def getfinalurl(self, urlt):
        parsed_url = urlparse(urlt)
        final_url = urlt
        soup = None
        urlhistory = None
        if not parsed_url.scheme:
            final_url = "http://" + urlt
        try:
            response = requests.get(final_url, allow_redirects=True, headers={
                                    'User-Agent': headers}, timeout=2)  # ,allow_redirects=True
            final_url = response.url
            soup = BeautifulSoup(response.text, 'html.parser')
            urlhistory = response.history
            return final_url, soup, urlhistory
        except requests.RequestException:
            return final_url, soup, urlhistory
        except Exception:
            return final_url, soup, urlhistory

    # ------------------------------------------------------ Extra Information------------------------------------------------------------
    def get_hostname(self):
        hostname = urlparse(self.url).hostname
        return hostname

    def get_domain(self):
        page_domain = tldextract.extract(self.url).domain
        return page_domain

    def get_subdomain(self):
        ext = tldextract.extract(self.url)
        subd = ext.subdomain
        subd_parts = subd.split('.')
        return subd_parts

    def get_scheme(self):
        htp = urlparse(self.url).scheme
        return htp

    def get_shorturl(self):
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
            return match.group()
        else:
            return None

    def get_ip_in_url(self):
        match = re.search(
            '(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
            '([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'  # IPv4
            # IPv4 in hexadecimal
            '((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)'
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', self.url)  # Ipv6
        if match:
            return match.group()
        else:
            return None

    def get_all_links(self):
        if self.soup:
            all_links = self.soup.find_all('a', href=True)
            return all_links
        return None

    def count_empty_links(self):
        if self.soup:
            empty_links_count = 0
            all_links = self.all_links
            for link in all_links:
                if '#' == link['href'][0] or link['href'] == '' or "javascript:void(0)" in link['href'] or "./" == link['href']:
                    empty_links_count += 1
            return empty_links_count
        return None

    def get_external_links(self):
        if self.soup:
            external_link_arr = []
            page_domain = self.domain
            all_links = self.all_links
            for link in all_links:
                if link['href'].split(":")[0] in ['http', 'https'] and not page_domain in link['href']:
                    external_link_arr.append(link['href'])
            return external_link_arr
        return None

    def get_img_requrl(self):
        if self.soup:
            img_requrls = self.soup.find_all('img', src=True)
            return img_requrls
        return None

    def get_audio_requrl(self):
        if self.soup:
            audio_requrls = self.soup.find_all('audio', src=True)
            return audio_requrls
        return None

    def get_embed_img_requrl(self):
        if self.soup:
            embed_requrls = self.soup.find_all('embed', src=True)
            return embed_requrls
        return None

    def get_iframe_requrl(self):
        if self.soup:
            iframe_requrls = self.soup.find_all('iframe', src=True)
            return iframe_requrls
        return None

    def get_external_img_requrl(self):
        if self.soup:
            external_img_arr = []
            page_domain = self.domain
            for img in self.img_requrl:
                if img['src'].split(":")[0] in ['http', 'https'] and not page_domain in img['src']:
                    external_img_arr.append(img['src'])
            return external_img_arr
        return None

    def get_external_audio_requrl(self):
        if self.soup:
            external_audio_arr = []
            page_domain = self.domain
            for audio in self.audio_requrl:
                if audio['src'].split(":")[0] in ['http', 'https'] and not page_domain in audio['src']:
                    external_audio_arr.append(audio['src'])
            return external_audio_arr
        return None

    def get_external_embed_requrl(self):
        if self.soup:
            external_embed_arr = []
            page_domain = self.domain
            for embed in self.embed_requrl:
                if embed['src'].split(":")[0] in ['http', 'https'] and not page_domain in embed['src']:
                    external_embed_arr.append(embed['src'])
            return external_embed_arr
        return None

    def get_external_iframe_requrl(self):
        if self.soup:
            external_iframe_arr = []
            page_domain = self.domain
            for iframe in self.iframe_requrl:
                if iframe['src'].split(":")[0] in ['http', 'https'] and not page_domain in iframe['src']:
                    external_iframe_arr.append(iframe['src'])
            return external_iframe_arr
        return None

    def get_external_favicon(self):
        if self.soup:
            favicon_link_arr = []
            page_domain = self.domain
            for favicon_link in self.soup.find_all('link', rel=['icon', 'shortcut icon']):
                if favicon_link['href'].split(":")[0] in ['http', 'https'] and not page_domain in favicon_link['href']:
                    favicon_link_arr.append(favicon_link['href'])
            return favicon_link_arr
        return None

    def get_creation_date(self):
        creation_date = self.w.creation_date
        if creation_date is None:
            creation_date = None
        elif type(creation_date) is list:
            creation_date = self.w.creation_date[0]
        elif type(creation_date) is str:
            creation_date = -1
        return creation_date

    def get_expiration_date(self):
        expiration_date = self.w.expiration_date
        if expiration_date is None:
            expiration_date = None
        elif type(expiration_date) is list:
            expiration_date = self.w.expiration_date[0]
        elif type(expiration_date) is str:
            expiration_date = -1
        return expiration_date

    def get_domainage(self):
        creation_date = self.creation_date
        expiration_date = self.expiration_date
        ageofdomain = 0
        if (expiration_date is None) or (creation_date is None):
            return 1
        elif creation_date == -1 or expiration_date == -1:
            return -1
        else:
            ageofdomain = abs((expiration_date - creation_date).days)
        return ageofdomain

    def get_domainend(self):
        expiration_date = self.expiration_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = 0
        if expiration_date is None:
            return 1
        elif expiration_date == -1:
            return -1
        else:
            registration_length = abs((expiration_date - today).days)
        return registration_length

    # -----------------------------------------------------------------Model Features---------------------------------------------------------------
    # 1 Get hostname length

    def getdomainlength(self):
        hostname = self.hostname
        if hostname:
            domain_length = len(hostname)
            return domain_length
        return -1

    # 2 Whether it contains www
    def contains_www(self):
        hostname = self.hostname
        if hostname:
            if "www" in hostname[0:3]:
                return 0
            else:
                return 1
        return -1

    # 3 has subdomain or not
    def has_subdomain(self):
        subd_parts = self.subdomains
        if subd_parts:
            if len(subd_parts) > 1:
                return 1
            else:
                return 0
        return -1

    # 4 checks https
    def httpSecure(self):
        htp = self.scheme
        match = str(htp)
        if htp:
            if match == 'https':
                return 0
            else:
                return 1
        return -1

    # 5 check http
    def http(self):
        htp = self.scheme
        match = str(htp)
        if htp:
            if match == 'https' or match == 'http':
                return 0
            else:
                return 1
        return -1

    # 6 short url
    def short_url(self):
        match = self.shortten_url
        if match:
            return 1
        else:
            return 0

    # 7 Use the IP Address
    def having_ip_address(self):
        match = self.get_ip_in_url()
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
        hostname = self.hostname
        if hostname:
            return hostname.count(".")
        return -1

    # 12
    def count_underscore_symbols(self):
        return self.url.count("_")

    # 13
    def count_slash_symbols(self):
        return self.url.count("/")

    # 14 count digit : tested
    def digit_count(self):
        hostname = self.hostname
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
        if self.soup:
            total_links_count = self.len_all_links
            empty_links_count = self.len_empty_links
            if total_links_count > 0:
                percentage_empty_links = (
                    empty_links_count / total_links_count) * 100
            else:
                percentage_empty_links = 0
            return percentage_empty_links
        else:
            return -1

    # 21 Percentage of links that lead to an external page.
    def calpc_extlinks(self):
        if self.soup:
            total_links_count = self.len_all_links
            external_links_count = self.len_external_links

            if total_links_count > 0:
                percentage_external_links = (
                    external_links_count / total_links_count) * 100
            else:
                percentage_external_links = 0

            return percentage_external_links
        else:
            return -1

    # 22 Percentage of external resources URL /Request URL ,examines whether the external objects contained within a webpage
    def calpc_requrl(self):
        if self.soup:
            total_requrl_count = self.len_all_requrl
            external_requrl_count = self.len_all_external_requrl

            if total_requrl_count > 0:
                percentage = (external_requrl_count /
                              float(total_requrl_count) * 100)
            else:
                percentage = 0
            return percentage
        else:
            return -1

    # 23 Zero links in body portion of HTML
    def haszerolinksinbody(self):
        if self.soup:
            body_links = self.soup.body.find_all('a', href=True)
            if len(body_links) == 0:
                return 1
            return 0
        else:
            return -1

    # 24 external favicon
    def has_external_favicon(self):
        if self.soup:
            external_favicon_count = self.len_external_favicon
            if external_favicon_count == 0:
                return 0
            else:
                return 1
        else:
            return -1

    # 25 submit2Email
    def submit2Email(self):
        if self.soup:
            if re.search(r"\b(mail\(\)|mailto:?)\b", self.soup.text, re.IGNORECASE):
                return 1
            else:
                return 0
        else:
            return -1

    # 26 SFHs that contain an empty string or “about:blank” are considered doubtful
    def sfh(self):
        if self.soup:
            domain = tldextract.extract(self.url).domain
            for form in self.soup.find_all('form', action=True):
                if form['action'] == "" or form['action'] == "about:blank":
                    return 1
                elif self.url not in form['action'] and domain not in form['action']:
                    return 1
                else:
                    return 0
            return 0
        else:
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
        ageofdomain = self.domain_age
        if ageofdomain is None:
            return 1
        elif ageofdomain == -1:
            return -1
        else:
            return 1 if (ageofdomain/30) < 6 else 0

    # 29 Domain Registration length
    def domainEnd(self):
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = self.domain_end
        if registration_length is None:
            return 1
        elif registration_length == -1:
            return -1
        else:
            return 1 if registration_length / 365 <= 1 else 0
