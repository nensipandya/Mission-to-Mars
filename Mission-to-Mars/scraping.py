# Add splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    # Excecute the path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    print(news_title)
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "Mars_hemispheres": mars_hemisphere(browser)
    }
    
    #stop webdriver and return data
    browser.quit()
    return data   


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    ## Convert the browser html to a soup object and then quit the browser

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
    
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find('div', class_="content_title").get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p
    
    except AttributeError:
        
        return None, None
    
    return news_title, news_p



# ### Featured Image
def featured_image(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_rel_url = img_soup.find('img', class_='fancybox-image').get('src')
        #img_rel_url
        
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_rel_url}'
        
     
    return(img_url)
    

## Mras Facts
def mars_facts():
    try:
        # Use read_html function to scrape the facts table into a DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe        
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #df

    # Convert dataframe into HTML format, add boodstrap
    df.to_html()

## Mars Hemisphere Information
def mars_hemisphere(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    
    html = browser.html
    names_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    hemisphere_image_urls = []
    
    names = names_soup.find_all('h3')

    for name in names:
        hemisphere_name = name.text
        
        element = browser.is_element_present_by_text(hemisphere_name, wait_time=2)
        if element == True:
            element_link = browser.links.find_by_partial_text(hemisphere_name)
            element_link.click()
            
            html = browser.html
            img_soup = soup(html, 'html.parser')
            
            img_url = img_soup.select_one("ul li a").get("href")
            
            hemispheres = {'img_url': img_url, 'title': hemisphere_name}
            
            hemisphere_image_urls.append(hemispheres)
            
        #Go back to original page
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
    return hemisphere_image_urls

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())

