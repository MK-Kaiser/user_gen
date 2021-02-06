#! /usr/bin/python3 

import requests
from bs4 import BeautifulSoup


class SurNames:
    def __init__(self):
        self.name_census_urls = ['https://namecensus.com/most_common_surnames.htm', 'https://namecensus.com/most_common_surnames1.htm', 'https://namecensus.com/most_common_surnames2.htm', 'https://namecensus.com/most_common_surnames5.htm', 'https://namecensus.com/most_common_surnames8.htm', 'https://namecensus.com/most_common_surnames12.htm', 'https://namecensus.com/most_common_surnames16.htm']
        self.session = requests.Session()

        # default no values
        self.surnames = []
    
    def inform_user(self, text, end='\n'):
        if not self.usernames_only:
            print(text, end=end)
        return

    def inform_debug(self, text):
        if self.debug:
            print(text)
        return
    
    def request(self):
        status = 'Gathering surnames'
        self.inform_user(status, end='\r')
        for url in self.name_census_urls:
            response = self.session.get(url)
            html = BeautifulSoup(response.content, 'html.parser')
            self.inform_debug(html.prettify)
            
            if response.status_code == 200:
                if html.find('table', {'id':'myTable'}):
                    self.__get_table__(html)
            
            status += '.'
            if not url == self.name_census_urls[-1]:
                self.inform_user(status, end='\r')
            else:
                self.inform_user(status)

            if self.count() >= self.top_surnames:
                self.inform_user(status)
                break #stop when we get to the max
        self.inform_user('Completed gathering surnames')
        self.surnames = self.surnames[:self.top_surnames] #cap off just the amount asked for
    
    def __get_table__(self, html):
        # if the top number is less than 1, it defaults to 10
        try:
            table = html.find('table', {'id':'myTable'})
            self.__extract_surnames__(table)
        except IndexError as identifier:
            print(identifier)
        except Exception as identifier:
            print(identifier)
        
        return
    
    def __extract_surnames__(self, table):
        try:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if columns:
                    self.surnames.append(columns[0].text.lower())
        except AttributeError as exception:
            # traceback.print_exc()
            raise exception
        except Exception as exception:
            # traceback.print_exc()
            raise exception
        return
    
    def count(self):
        return len(self.surnames)

    def dedupe_surnames(self):
        self.surnames = list(set(self.surnames))
