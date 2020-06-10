# Scraping News
import html
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup
import os
import urllib.request
from sys import platform
import sqlite3
import time

def news_fetch():
    cwd = os.getcwd()

    if platform == "linux" or platform == "linux2":
        cwd += "/main_app"
    else:
        cwd += "\main_app"
    # Updating db
    conn = sqlite3.connect('newsdb.db')
    # print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS News_content(Id Int,headline Varchar,summary Varchar,url Varchar, date Varchar);')
    conn.execute("delete from News_content")



    urlList = ['https://economictimes.indiatimes.com/topic/women/news']
    baseURL = 'https://economictimes.indiatimes.com'

    for url in urlList:
        req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = soup(webpage,"html.parser")

        # fetching links of articles on Home page
        tags_lst = []
        divTag = page_soup.find_all('div', class_= 'flr topicstry')
        tags_lst.append(divTag)
        divTag = page_soup.find_all('div', class_= 'clr flt topicstry')
        tags_lst.append(divTag)

        news = 0
        for divTag in tags_lst:
            for tag in divTag:
                head = tag.find("h3")
                para = tag.find("p")
                tdTags = tag.find("a")
                date = tag.find("time")
                # img = tag.find("img")
                if head!=None:
                    head = head.text
                    # print(head)
                else:
                    continue
                if para!=None:
                    para = para.text
                    # print(para)
                else:
                    continue
                if date!=None:
                    date = date.text
                    # print(date)
                else:
                    continue
                if tdTags!=None:
                    url = tdTags.get("href")
                    url = baseURL+str(url)
                    # print(url)
                else:
                    continue
                if head!=None and para!=None and url!=None and date!=None:
                    # if platform == "linux" or platform == "linux2":
                    #     fullfilename = os.path.join(cwd + "/static/Pics", str(news + 1) + ".jpg")
                    # else:
                    #     fullfilename = os.path.join(cwd + "\main_app\static\Pics", str(news + 1) + ".jpg")
                    # urllib.request.urlretrieve(img_url, fullfilename)

                    query = "INSERT INTO News_content (Id,headline,summary,url, date) VALUES (?, ?, ?, ?, ?) "
                    recordTuple = (news + 1, head, para, url, date)
                    conn.execute(query, recordTuple)
                    news+=1

    conn.commit()
    # print("Done")
    e = time.time()
    # print("total time", e-s)
    conn.close()

# news_fetch()

def write_news():

    cwd = os.getcwd()
    file_name = cwd

    if platform == "linux" or platform == "linux2":
        file_name +=   "/main_app/templates/main_app/news.html"
    else:
        file_name += "\main_app\\templates\main_app\\news.html"
    # print(file_name)
    file = open(file_name, "w+")
    conn = sqlite3.connect('newsdb.db')
    # print("Opened database successfully")
    cur = conn.cursor()
    cur.execute('SELECT * FROM News_content;')
    results = cur.fetchall()
    news_count = len(results)
    conn.close()
    # print(len(results), results)
    cards = []
    count = 1
    for j in results:
        card = """  <div class="card" style="margin-left:20px">
                        <div class="card-image waves-effect waves-block waves-light">
                            <img height="200" class="activator" src="{% static 'Pics/""" + str(count) +""".jpg' %}">
                        </div>
                        <div class="card-content">
                            <span class="card-title activator grey-text text-darken-4">""" + j[1] +"""<i class="material-icons right">more_vert</i></span>
                            <p><a style="color:white; background-color:black;" class="waves-effect waves-light btn" target="_blank" href="  """ + j[3] + """  ">See More</a></p>
                        </div>
                        <div class="card-reveal">
                        <span class="card-title activator grey-text text-darken-4">""" + j[4] +"""
                          <i class="material-icons right">close</i>
                          <p class="activator">""" + j[2] +"""</p></span>
                        </div>
                     </div>"""

        cards.append(card)
        count +=1

    file.write("""
                    <!DOCTYPE html>
                    {% extends 'main_app/common.html' %}
                    {% load static %}    
                
                    {% block content %} 
                    <br>
                    <body>
                    <div style="max-width:80%; margin-left:auto; margin-right:auto; display:block;" >
                    <div class="jumbotron">
                      <h1 class="display-4">Latest news!!</h1>
                      <p class="lead">News and issues of women should no longer go unnoticed, know the real issues.</p>
                      <hr class="my-4">
                      <p class="lead">
                        <a style="color:white; background-color:black;" class="btn btn-primary btn-lg tooltipped" href="{% url 'main_app:news' %}" role="button"  data-position="right" data-tooltip="Refresh for latest news">Refresh</a>
                      </p>
                    </div>
                    <style>.card { width:400px; height:400px;} </style>
                       <div class="row" style="margin-left:8%;"> """)

    for card in cards:
        file.write(card)

    file.write(""" </div></div>
                    </body>
                        {% endblock %} """)

    file.close()

# s = time.time()
#
# news_fetch()

# write_news()
#
# e = time.time()
#
# print((e-s)/1000)
