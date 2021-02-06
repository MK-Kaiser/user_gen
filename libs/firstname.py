#! /usr/bin/python3

import requests
from datetime import datetime
from bs4 import BeautifulSoup

CURRENT_YEAR = int(datetime.now().year)

class FirstNames:
    def __init__(self):
        self.session = requests.Session()
        self.ssa_site_url = 'https://www.ssa.gov/cgi-bin/popularnames.cgi'
        
        # default no values
        self.males = []
        self.females = []
        self.combined = []
        
    def inform_user(self, text):
        if not self.usernames_only:
            print(text)
        return

    def inform_debug(self, text):
        if self.debug:
            print(text)
        return


    def request(self):
        for year in range(0, self.years):
            data = {}
            data['year'] = CURRENT_YEAR - year
            data['top'] = abs(self.top_firstnames)
        
            response = self.session.post(self.ssa_site_url, data=data)
            html = BeautifulSoup(response.content, 'html.parser')
            self.inform_debug(html.prettify)
            if response.status_code == 200:
                if not response.content.find(b'are not available') == -1:
                    self.inform_user('There seems to be no results for year {}'.format(data['year']))
                elif not response.content.find(b'Unable to find data for year of birth') == -1:
                    self.inform_user('Unable to find data for year of birth {}'.format(data['year']))
                elif not response.content.find(b'Popularity in') == -1:
                    self.inform_user('Results discvoered for birth year of {}'.format(data['year']))
                    self.__get_table__(html)
                else:
                    self.inform_debug(html.prettify)
            else:
                self.inform_user('Received a non-200 reponse code')
                self.inform_debug(html.prettify)
        return
    
    def __get_table__(self, html):
        # if the top number is less than 1, it defaults to 10
        summary = "Popularity for top 10"
        if self.top_firstnames:
            summary = "Popularity for top {}".format(self.top_firstnames)
        try:
            table = html.find_all('table', {"summary":summary})[0]
            self.__extract_names__(table)
        except IndexError as identifier:
            print(identifier)
        except Exception as identifier:
            print(identifier)
        
        return
    
    def __extract_names__(self, table):
        try:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 2:
                    self.males.append(columns[1].text.lower())
                    self.females.append(columns[2].text.lower())
        except AttributeError as exception:
            raise exception
        except Exception as exception:
            raise exception

        return
    
    def dedupe_names(self):
        self.males = list(set(self.males))
        self.females = list(set(self.females))
        self.combined = self.males + self.females
        self.combined = list(set(self.combined))
