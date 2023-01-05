import os

import requests
from bs4 import BeautifulSoup
from facebook_scraper import get_posts, get_profile
from lxml import etree
from core.web_driver import WebDriver
import re


class BeautifulSoupScrape:
    def __init__(self, page_sources, link):
        self.person = {}
        self.data = {}
        self.page_sources = page_sources
        self.person['url_fb'] = link
        self.soup = None

    def about(self):
        try:
            for k, v in self.page_sources.items():
                explicit_data = []
                self.soup = BeautifulSoup(v, "html.parser")
                extract = self.soup.find('div', class_='xyamay9 xqmdsaz x1gan7if x1swvt13')
                for i in extract.strings:
                    explicit_data.append(str(i))
                self.data[k] = explicit_data

            for k, v in self.data.items():
                if k == 'about_places':
                    if 'No places to show' in v:
                        self.person[k] = {v[0]: v[1]}
                    else:
                        v.remove('Places lived')
                        result = [v[i] for i in range(len(v)) if i % 2 == 1]
                        result2 = [v[i] for i in range(len(v)) if i % 2 != 1]
                        self.person[k] = (dict(zip(result, result2)))

                if k == 'about_work_and_education':
                    data = ''
                    dict_work = {}
                    for i in v:
                        if i == 'College':
                            dict_work['Work'] = data[:-1]
                            data = ''
                        elif i == "High school":
                            dict_work['College'] = data[:-1]
                            data = ''
                        elif len(v) - 1 == v.index(i):
                            dict_work['High School'] = data + i
                        elif i == 'Work':
                            pass
                        else:
                            data += i + " "
                    self.person[k] = dict_work

                if k == 'about_contact_and_basic_info':
                    v.remove('Basic info')
                    result = [v[i] for i in range(len(v)) if i % 2 == 1]
                    result2 = [v[i] for i in range(len(v)) if i % 2 != 1]
                    self.person[k] = (dict(zip(result2, result)))

                if k == 'about_family_and_relationships':
                    data = {v[0]: v[1]}
                    v = v[3:]
                    result = [v[i] for i in range(len(v)) if i % 2 == 1]
                    result2 = [v[i] for i in range(len(v)) if i % 2 != 1]
                    data['Family members'] = (dict(zip(result, result2)))
                    self.person[k] = data

                if k == 'about_details':
                    if 'Nickname' in v:
                        v.remove("Other names")
                    result = [v[i] for i in range(len(v)) if i % 2 == 1]
                    result2 = [v[i] for i in range(len(v)) if i % 2 != 1]
                    result2[0] = 'About'
                    self.person[k] = (dict(zip(result2, result)))

                if k == 'about_life_events':
                    dict_events = {}
                    events = ''
                    year = v[0]
                    for i in v:
                        events += i + '\n'
                        if re.findall(r"^20", i) or len(v) - 1 == v.index(i):
                            dict_events[year] = events[:-1]
                            year = i
                            events = ''
                            continue
                    self.person[k] = dict_events

            # Name
            name = self.soup.find('h1', {'class': 'x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz'}).text
            basic_name = ''
            for i in name:
                if i == "ă" or i == "â":
                    basic_name += "a"
                elif i == "ţ":
                    basic_name += "t"
                elif i == "ș":
                    basic_name += "s"
                elif i == "î":
                    basic_name += "i"
                else:
                    basic_name += i

            self.person['name'] = basic_name

            # No. of friends
            friends = self.soup.find('a', {
                'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r '
                         'x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq '
                         'x1a2a7pz xt0b8zv xi81zsa x1s688f'})
            if friends:
                self.person['friends'] = friends.text.split(' ')[0]
            elif friends is None:
                self.person['friends'] = "Private"

            posts = []
            id = self.person['url_fb'].split("/")[-1]
            nr_post = 0
            try:
                while nr_post < 5:
                    for post in get_posts(id, credentials=(os.environ['user'], os.environ['pass'])):
                        posts.append({'post_id': post['post_id'], 'post_text': post['post_text'], 'time': post['time'],
                                      'image': post['image'], 'likes': post['likes'], 'comments': post['comments'],
                                      'shares': post['shares'], 'post_url': post['post_url']})
                        nr_post += 1
            except:
                posts = "No posts found"
            self.person['posts'] = posts
            return self.person
        except Exception as e:
            print("Can't scrape the person --> ", str(e))
