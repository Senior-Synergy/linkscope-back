import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from pysafebrowsing import SafeBrowsing
from datetime import datetime
import tldextract
import whois
import time
import re
import requests
import socket


dotenv_path = '.env'
load_dotenv(dotenv_path)

google_api_key = os.getenv('GOOGLE_API_KEY')

headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0'
]


class URLFeatures:
    def __init__(self, url_input):
        url_data = self.get_url_data(url_input)

        self.final_url = url_data[0]
        self.soup = url_data[1]
        self.url_history = url_data[2]

        self.hostname = self.get_hostname()
        self.domain = self.get_domain()
        self.subdomains = self.get_subdomain()
        self.scheme = self.get_scheme()
        self.ip = self.get_ip_address()
        self.shortten_url = self.get_shorturl()
        self.ip_in_url = self.get_ip_in_url()

        # all links
        self.all_links = self.get_all_links()

        # count empty link
        self.empty_links_count = self.count_empty_links()

        # all img, audio, embed, iframe requrl
        self.img_requrl = self.get_img_requrl()
        self.audio_requrl = self.get_audio_requrl()
        self.embed_requrl = self.get_embed_img_requrl()
        self.iframe_requrl = self.get_iframe_requrl()

        # external links
        self.external_links = self.get_external_links()

        # external requrl
        self.external_img_requrl = self.get_external_img_requrl()
        self.external_audio_requrl = self.get_external_audio_requrl()
        self.external_embed_requrl = self.get_external_embed_requrl()
        self.external_iframe_requrl = self.get_external_iframe_requrl()

        # external favicon
        self.external_favicon = self.get_external_favicon()

        try:
            self.whois = whois.whois(self.hostname)
        except Exception:
            self.whois = None

        # domain creation date and expiration date
        self.creation_date = self.get_creation_date()
        self.expiration_date = self.get_expiration_date()

        # Age of domain and registration length of domain
        self.domain_age = self.get_domainage()
        self.domain_end = self.get_domainend()

    def get_model_features(self):
        return {
            'domainlength': self.getdomainlength(),
            'www': self.contains_www(),
            'https': self.httpSecure(),
            'short_url': self.short_url(),
            'ip': self.having_ip_address(),
            'dash_count': self.count_dash_symbols(),
            'equal_count': self.count_equal_symbols(),
            'dot_count': self.count_dot_symbols(),
            'underscore_count': self.count_underscore_symbols(),
            'slash_count': self.count_slash_symbols(),
            'digit_count': self.digit_count(),
            'pc_emptylink': self.calc_pc_emptylinks(),
            'pc_extlink': self.calc_pc_extlinks(),
            'pc_requrl': self.calc_pc_requrl(),
            'zerolink': self.has_zero_links_in_body(),
            'ext_favicon': self.has_external_favicon(),
            'sfh':  self.sfh(),
            'redirection': self.redirection(),
            'domainend': self.domainEnd() if self.whois else -1
        }

    def get_extra_features(self):
        return {
            'shortten_url': self.shortten_url,
            'ip_in_url': self.ip_in_url,
            'empty_links_count': self.empty_links_count,
            'external_links': self.external_links,
            'external_img_requrl': self.external_img_requrl,
            'external_audio_requrl': self.external_audio_requrl,
            'external_embed_requrl': self.external_embed_requrl,
            'external_iframe_requrl': self.external_iframe_requrl,
            'len_external_links': len(self.external_links) if self.external_links is not None else None,
            'len_external_img_requrl': len(self.external_img_requrl) if self.external_img_requrl is not None else None,
            'len_external_audio_requrl': len(self.external_audio_requrl) if self.external_audio_requrl is not None else None,
            'len_external_embed_requrl': len(self.external_embed_requrl) if self.external_embed_requrl is not None else None,
            'len_external_iframe_requrl': len(self.external_iframe_requrl) if self.external_iframe_requrl is not None else None,
        }

    def get_extra_url_info(self):
        return {
            # extra url info
            'hostname': self.hostname,
            'domain': self.domain,
            'registrar': self.get_domain_registrar(),
            'ip_address': self.ip,
            'subdomains': self.subdomains,
            'scheme': self.scheme,
            # extra domain infomation
            'creation_date': self.creation_date,
            'expiration_date': self.expiration_date,
            'domainage': self.domain_age,
            'domainend': self.domain_end,
            'city':  self.get_city(),
            'state': self.get_state(),
            'country': self.get_country(),
            'google_is_malicious': self.get_google_is_malicious()
        }

    # 0.UsingIp

    def get_url_data(self, urlt):
        parsed_url = urlparse(urlt)
        final_url = urlt
        soup = None
        urlhistory = None

        if not parsed_url.scheme:
            final_url = "http://" + urlt

        for user_agent in user_agents:
            try:
                response = requests.get(final_url, allow_redirects=True, headers={
                                        'User-Agent': user_agent}, timeout=2)  # allow_redirects=True

                final_url = response.url
                soup = BeautifulSoup(response.text, 'html.parser')
                urlhistory = response.history

                return final_url, soup, urlhistory
            except Exception:
                continue

        # If all user agents fail, return None for all variables
        return final_url, soup, urlhistory

        # try:
        #     response = requests.get(final_url, allow_redirects=True, headers={
        #                             'User-Agent': headers}, timeout=2)  # ,allow_redirects=True
        #     final_url = response.url
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     urlhistory = response.history
        #     return final_url, soup, urlhistory
        # except requests.RequestException:
        #     return final_url, soup, urlhistory
        # except Exception:
        #     return final_url, soup, urlhistory

    # ------------------------------------------------------ Extra Information------------------------------------------------------------

    def get_hostname(self):
        hostname = urlparse(self.final_url).hostname
        return hostname

    def get_domain(self):
        page_domain = tldextract.extract(self.final_url).domain
        return page_domain

    def get_subdomain(self):
        ext = tldextract.extract(self.final_url)
        subd = ext.subdomain
        if subd:
            subd_parts = subd.split('.')
            return subd_parts
        return None

    def get_scheme(self):
        htp = urlparse(self.final_url).scheme
        return htp

    def get_shorturl(self):
        pattern = r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|' \
            r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|' \
            r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|' \
            r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|' \
            r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|' \
            r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|' \
            r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|' \
            r'tr\.im|link\.zip\.net'
        match = re.search(pattern, self.final_url)
        if match:
            return match.group()
        else:
            return None

    def get_ip_in_url(self):
        pattern = r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.' \
            r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'  \
            r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)' \
            r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}'
        match = re.search(
            pattern, self.final_url)
        if match:
            return match.group()
        else:
            return None

    def get_all_links(self):
        if self.soup is None:
            return None

        all_links = self.soup.find_all('a', href=True)

        return all_links

    def count_empty_links(self):
        if self.soup is None or self.all_links is None:
            return None

        empty_links_count = 0
        all_links = self.all_links

        for link in all_links:
            href = link.get('href', '')
            if href.startswith('#') or href == '' or "javascript:void(0)" in href or href.startswith("./"):
                empty_links_count += 1

        return empty_links_count

    def get_external_links(self):
        # Cannot obtain either soup or all_links from soup
        if self.soup is None or self.all_links is None:
            return None

        external_link_arr = []
        all_links = self.all_links

        page_domain = self.domain
        for link in all_links:
            if link['href'].split(":")[0] in ['http', 'https'] and not page_domain in link['href']:
                external_link_arr.append(link['href'])

        return external_link_arr

    def get_img_requrl(self):
        if self.soup is None:
            return None

        img_requrls = self.soup.find_all('img', src=True)
        return img_requrls

    def get_audio_requrl(self):
        if self.soup is None:
            return None

        audio_requrls = self.soup.find_all('audio', src=True)
        return audio_requrls

    def get_embed_img_requrl(self):
        if self.soup is None:
            return None

        embed_requrls = self.soup.find_all('embed', src=True)
        return embed_requrls

    def get_iframe_requrl(self):
        if self.soup is None:
            return None

        iframe_requrls = self.soup.find_all('iframe', src=True)
        return iframe_requrls

    def get_external_img_requrl(self):
        if self.soup is None or self.img_requrl is None:
            return None

        external_img_arr = []
        page_domain = self.domain

        for img in self.img_requrl:
            if img['src'].split(":")[0] in ['http', 'https'] and not page_domain in img['src']:
                external_img_arr.append(img['src'])

        return external_img_arr

    def get_external_audio_requrl(self):
        if self.soup is None or self.audio_requrl is None:
            return None

        external_audio_arr = []
        page_domain = self.domain

        for audio in self.audio_requrl:
            if audio['src'].split(":")[0] in ['http', 'https'] and not page_domain in audio['src']:
                external_audio_arr.append(audio['src'])

        return external_audio_arr

    def get_external_embed_requrl(self):
        if self.soup is None or self.embed_requrl is None:
            return None

        external_embed_arr = []

        page_domain = self.domain
        for embed in self.embed_requrl:
            if embed['src'].split(":")[0] in ['http', 'https'] and not page_domain in embed['src']:
                external_embed_arr.append(embed['src'])

        return external_embed_arr

    def get_external_iframe_requrl(self):
        if self.soup is None or self.iframe_requrl is None:
            return None

        external_iframe_arr = []
        page_domain = self.domain

        for iframe in self.iframe_requrl:
            if iframe['src'].split(":")[0] in ['http', 'https'] and not page_domain in iframe['src']:
                external_iframe_arr.append(iframe['src'])

        return external_iframe_arr

    def get_external_favicon(self):
        if self.soup is None:
            return None

        favicon_link_arr = []
        page_domain = self.domain

        for favicon_link in self.soup.find_all('link', rel=['icon', 'shortcut icon']):
            if favicon_link['href'].split(":")[0] in ['http', 'https'] and not page_domain in favicon_link['href']:
                favicon_link_arr.append(favicon_link['href'])

        return favicon_link_arr

    def get_ip_address(self):
        if self.hostname:
            IP_addr = socket.gethostbyname(self.hostname)

            if IP_addr:
                return IP_addr
            else:
                return None
        else:
            return None

    def get_domain_registrar(self):
        if self.whois is None or self.whois.registrar is None:
            return None

        return self.whois.registrar

    def get_city(self):
        if self.whois is None or self.whois.city is None:
            return None

        city_value = self.whois.city

        if isinstance(city_value, str):
            if city_value.strip() and city_value.strip().upper() not in ['REDACTED FOR PRIVACY', 'DATA REDACTED']:
                return city_value.strip()  # Return the stripped city value
        return None

    def get_state(self):
        if self.whois is None or self.whois.state is None or self.whois.state in ['REDACTED FOR PRIVACY', 'DATA REDACTED']:
            return None

        return self.whois.state

    def get_country(self):
        if self.whois is None or self.whois.country is None or self.whois.country in ['REDACTED FOR PRIVACY', 'DATA REDACTED']:
            return None

        return self.whois.country

    def get_creation_date(self):
        if self.whois is None or self.whois.creation_date is None:
            return None

        creation_date = self.whois.creation_date

        if type(creation_date) is list:
            creation_date = creation_date[0]

        if isinstance(creation_date, str):
            creation_date = datetime.strptime(creation_date, "%Y-%m-%d")

        return creation_date

    def get_expiration_date(self):
        if self.whois is None or self.whois.expiration_date is None:
            return None

        expiration_date = self.whois.expiration_date

        if type(expiration_date) is list:
            expiration_date = expiration_date[0]

        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")

        return expiration_date

    def get_domainage(self):
        if self.whois is None or self.creation_date is None or self.expiration_date is None:
            return -1

        creation_date = self.creation_date
        expiration_date = self.expiration_date

        ageofdomain = 0
        ageofdomain = abs((expiration_date - creation_date).days)

        return ageofdomain

    def get_domainend(self):
        if self.whois is None or self.expiration_date is None:
            return -1

        expiration_date = self.expiration_date
        today = datetime.today()

        registration_length = 0
        registration_length = abs((expiration_date - today).days)

        return registration_length

    def get_google_is_malicious(self):
        s = SafeBrowsing(google_api_key)
        r = s.lookup_urls([self.final_url])

        if r:
            return r[self.final_url].get('malicious', None)
        else:
            return None

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

    # 3 checks https
    def httpSecure(self):
        htp = self.scheme
        match = str(htp)
        if htp:
            if match == 'https':
                return 0
            else:
                return 1
        return -1

    # 4 short url
    def short_url(self):
        match = self.shortten_url
        if match:
            return 1
        else:
            return 0

    # 5 Use the IP Address
    def having_ip_address(self):
        match = self.get_ip_in_url()
        if match:
            return 1
        else:
            return 0

    # 6
    def count_dash_symbols(self):
        return self.final_url.count("-")

    # 7
    def count_equal_symbols(self):
        return self.final_url.count("=")

    # 8
    def count_dot_symbols(self):
        hostname = self.hostname
        if hostname:
            return hostname.count(".")
        return -1

    # 9
    def count_underscore_symbols(self):
        return self.final_url.count("_")

    # 10
    def count_slash_symbols(self):
        return self.final_url.count("/")

    # 11 count digit : tested
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

    # 12 Percentage of links that do not lead to another page
    def calc_pc_emptylinks(self):
        if self.soup is None:
            return -1

        total_links_count = len(self.all_links) if self.all_links else 0
        empty_links_count = self.empty_links_count if self.empty_links_count else 0

        if total_links_count > 0:
            percentage_empty_links = (
                empty_links_count / total_links_count) * 100
        else:
            percentage_empty_links = 0
        return percentage_empty_links

    # 13 Percentage of links that lead to an external page.

    def calc_pc_extlinks(self):
        if self.soup is None:
            return -1

        total_links_count = len(self.all_links) if self.all_links else 0
        external_links_count = len(
            self.external_links) if self.external_links else 0

        if total_links_count > 0:
            percentage_external_links = (
                external_links_count / total_links_count) * 100
        else:
            percentage_external_links = 0

        return percentage_external_links

    # 14 Percentage of external resources URL /Request URL ,examines whether the external objects contained within a webpage
    def calc_pc_requrl(self):
        if self.soup is None:
            return -1

        total_requrl_count = len(self.img_requrl) if self.img_requrl else 0 + len(self.audio_requrl) if self.audio_requrl else 0 + len(
            self.embed_requrl) if self.embed_requrl else 0 + len(self.iframe_requrl) if self.iframe_requrl else 0
        external_requrl_count = len(self.external_img_requrl) if self.external_img_requrl else 0 + len(self.external_audio_requrl) if self.external_audio_requrl else 0 + len(
            self.external_embed_requrl) if self.external_embed_requrl else 0 + len(self.external_iframe_requrl) if self.external_iframe_requrl else 0

        if total_requrl_count > 0:
            percentage = (external_requrl_count /
                          float(total_requrl_count) * 100)
        else:
            percentage = 0
        return percentage

    # 15 Zero links in body portion of HTML
    def has_zero_links_in_body(self):
        if self.soup is None or self.soup.body is None:
            return -1

        body_links = self.soup.body.find_all('a', href=True)
        if len(body_links) == 0:
            return 1
        return 0

    # 16 external favicon
    def has_external_favicon(self):
        if self.soup is None:
            return -1

        external_favicon_count = len(
            self.external_favicon) if self.external_favicon else 0
        if external_favicon_count == 0:
            return 0
        else:
            return 1

    # 17 SFHs that contain an empty string or “about:blank” are considered doubtful

    def sfh(self):
        if self.soup is None:
            return -1

        domain = tldextract.extract(self.final_url).domain
        for form in self.soup.find_all('form', action=True):
            if form['action'] == "" or form['action'] == "about:blank":
                return 1
            elif self.final_url not in form['action'] and domain not in form['action']:
                return 1
            else:
                return 0
        return 0

    # 18 redirection
    def redirection(self):
        if self.url_history is None:
            return -1

        if len(self.url_history) > 1:
            return 1
        else:
            return 0

    # 19 Domain Registration length
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
