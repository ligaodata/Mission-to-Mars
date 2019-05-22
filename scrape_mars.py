
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    ### Get Mars News
    executable_path = {"executable_path" : "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find("div", class_="content_title").text
    news_para = soup.find("div", class_="article_teaser_body").text

    ### Get Mars Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve full size image url
    article = soup.find("li",class_="slide")
    featured_image_url=article.find("img",class_='thumb')['src']
    # Get full url
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url

    ### Get Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    weather_list = soup.find_all("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    # Make sure the data we get is valid and complete which should include with "high" "low" "gusting"
    for weather in weather_list:
        try:
            mars_weather = weather.text
            mars_weather_1 = [i.lower() for i in mars_weather.split(" ")]
            if ("low" in mars_weather_1) and ("high" in mars_weather_1) and ("gusting" in mars_weather_1):
                if mars_weather_1[-1].split(".")[0]=="hpapic" :
                    mars_weather = mars_weather[:-26]
            print(mars_weather)
            break
           
        except:
            pass   


    ### Get Mars Facts

    # Use Panda's `read_html` to parse the url
    url="https://space-facts.com/mars/"
    tables = pd.read_html(url)
    Mars_df = tables[0]

    Mars_df = Mars_df.rename(columns={0:"Description",1:"Value"})
    Mars_df.set_index("Description",inplace=True)

    # Convert dataframe to html table
    mars_facts_html = Mars_df.to_html().replace("\n","")
    mars_facts_html = mars_facts_html.replace("right","center")
    #display(mars_facts_html)
    print(mars_facts_html)


    ### Get Hemisphere Images

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_list = []

    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]
    for x in range(0,4):
        browser.click_link_by_partial_text(hemispheres[x])
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        img_url = "https://astrogeology.usgs.gov" + (soup.find("img", class_="wide-image")["src"])
        title = (soup.find("h2", class_="title").text)
        
        hemisphere_dict = {"title": title, "img_url":img_url}
        hemisphere_list.append(hemisphere_dict)
        
        browser.back()
 
    browser.quit()

        # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_para": news_para,
        "featured_image_url": featured_image_url,
        "weather_report" : mars_weather,
        "mars_facts_html" : mars_facts_html,
        "hemisphere_list" : hemisphere_list
    }

    return mars_data












