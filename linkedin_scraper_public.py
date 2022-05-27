from os import name
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select



#accessing Chromedriver
browser = webdriver.Chrome(ChromeDriverManager().install())


#Replace with you username and password
username =  
password =  

#Open login page
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

#Enter login info:
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()
lolol='grooveventures'
#lol=['https://www.linkedin.com/company/aleph-vc/posts']
#Go to company webpage
browser.get('https://www.linkedin.com/company/grove-ventures/posts')

time.sleep(6)
#browser.find_element_by_class_name('msg-overlay-list-bubble__default-conversation-container').click() 


# element = browser.find_element_by_css_selector('#ember74')


browser.execute_script("document.getElementsByClassName('artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view display-flex t-normal t-12 t-black--light')[0].click(); ")

# actions = ActionChains(browser)
# actions.move_to_element(element).click().perform()
time.sleep( 3)
# element = browser.find_element_by_css_selector('#ember75')
# time.sleep(2)
# actions = ActionChains(browser)
# actions.move_to_element(element).click().perform()
# time.sleep(2)

#browser.execute_script("document.getElementByCssSelector('#ember75')[0].click(); ")

#browser.execute_script("document.getElementsById('artdeco-dropdown__content artdeco-dropdown--is-dropdown-element artdeco-dropdown__content--justification-right artdeco-dropdown__content--placement-bottom ember-view')[0].click(); ")
#Select(browser.find_element_by_id('ember75'))
element = browser.find_element_by_css_selector('#ember76')
time.sleep(2)
actions = ActionChains(browser)
actions.move_to_element(element).click().perform()
time.sleep(2)


#browser.execute_script('document.getelementByClassName('sort-dropdown__icon').click() )

#browser.find_element_by_css_selector('#ember74').click()
time.sleep(5)
#browser.find_element_by_class_name('artdeco-dropdown__content artdeco-dropdown--is-dropdown-element artdeco-dropdown__content--justification-right artdeco-dropdown__content--placement-bottom ember-view').click()

#elementID.find_element_by_name('posts')

#Simulate scrolling to capture all posts
SCROLL_PAUSE_TIME = 4

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
count=0
while  count<40:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('Scroll=')
    print(count)
    print('end')
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    count=count+1
    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


    
#Check out page source code
company_page = browser.page_source   



# #Import exception check for message popups (not needed atm)
# from selenium.common.exceptions import NoSuchElementException
# try:
#     if browser.find_element_by_class_name('msg-overlay-list-bubble--is-minimized') is not None:
#         pass
# except NoSuchElementException:
#     try:
#         if browser.find_element_by_class_name('msg-overlay-bubble-header') is not None:
#             browser.find_element_by_class_name('msg-overlay-bubble-header').click()
#     except NoSuchElementException:
#         pass


#Use Beautiful Soup to get access tags
linkedin_soup = bs(company_page.encode("utf-8"), "html" )
linkedin_soup.prettify()
 

#Find the post blocks
containers = linkedin_soup.findAll("div",{"class":"occludable-update ember-view"})
container = containers[0].find("div","feed-shared-update-v2__description-wrapper ember-view")


# Lists that we will iterate to
post_dates = []
post_texts = []
post_likes = []
post_comments = []
video_views = []
media_links = []
media_type = []
post_link=[]


#Looping through the posts and appending them to the lists
for container in containers:
    
    try:
        posted_date = container.find("span",{"class":"visually-hidden"})
        text_box = container.find("div",{"class":"feed-shared-update-v2__description-wrapper ember-view"})
        text = text_box.find("span",{"dir":"ltr"})
        new_likes = container.findAll("li", {"class":"social-details-social-counts__reactions social-details-social-counts__item"})
        new_comments = container.findAll("li", {"class": "social-details-social-counts__comments social-details-social-counts__item"})
       # new_link = container.findAll( 'a'  )
        
        # new_lnk= new_link 
        # print( new_link['href'] )


        #Appending date and text to lists
        post_dates.append(posted_date.text.strip())
        post_texts.append(text_box.text.strip())


        #Determining media type and collecting video views if applicable
        try:
            video_box = container.findAll("div",{"class": "feed-shared-update-v2__content feed-shared-linkedin-video ember-view"})
            video_link = video_box[0].find("video", {"class":"vjs-tech"})
            media_links.append(video_link['src'])
            media_type.append("Video")
        except:
            try:
                image_box = container.findAll("div",{"class": "feed-shared-image__container"})
                image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image feed-shared-image__image--constrained lazy-image ember-view"})
                media_links.append(image_link['src'])
                media_type.append("Image")
            except:
                try:
                    image_box = container.findAll("div",{"class": "feed-shared-image__container"})
                    image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image lazy-image ember-view"})
                    media_links.append(image_link['src'])
                    media_type.append("Image")
                except:
                    try:
                        article_box = container.findAll("div",{"class": "feed-shared-article__link-container"})
                        article_link = article_box[0].find("a", {"class":"feed-shared-article__image-link tap-target app-aware-link ember-view"})
                        media_links.append(article_link['href'])
                        media_type.append("Article")
                    except:
                        try:
                            poll_box = container.findAll("div",{"class": "feed-shared-update-v2__content overflow-hidden feed-shared-poll ember-view"})
                            media_links.append("None")
                            media_type.append("Other (Shared Post/Poll, etc.)")
                        except:
                            media_links.append("None")
                            media_type.append("Unknown")



        #Getting Video Views. (The folling three lines prevents class name overlap)
        view_container2 = set(container.findAll("li", {'class':["social-details-social-counts__item"]}))
        view_container1 = set(container.findAll("li", {'class':["social-details-social-counts__reactions","social-details-social-counts__comments social-details-social-counts__item"]}))
        result = view_container2 - view_container1

        view_container = []
        for i in result:
            view_container += i

        try:
            video_views.append(view_container[1].text.strip().replace(' Views',''))

        except:
            video_views.append('N/A')

        
        #Appending likes and comments if they exist
        try:
            post_likes.append(new_likes[0].text.strip())
        except:
            post_likes.append(0)
            pass

        try:
            post_comments.append(new_comments[0].text.strip())                           
        except:                                                           
            post_comments.append(0)
            pass
        try:
            post_link.append(new_link[0] )                                
        except:                                                           
            post_link.append(0)
            pass        
    except:
        pass

    
# #Cleaning the dates
# cleaned_dates = []
# for i in post_dates:
#     d = str(i[0:3]).replace('\n\n', '').replace('•','').replace(' ', '')
#     cleaned_dates += [d]


#Stripping non-numeric values
comment_count = []
for i in post_comments:
    s = str(i).replace('Comment','').replace('s','').replace(' ','')
    comment_count += [s]


    
#Constructing Pandas Dataframe
data = {
    "Post Content": post_texts,
    "Date of Publishing": post_dates,
    "Post Likes": post_likes,
    "Post Comments": comment_count,
    "Video Views": video_views,

    "Media Type": media_type,
    
    
    "Media Links": media_links,
#     "Post Link": post_link
}

df = pd.DataFrame(data)


#Exporting csv to program folder
df.to_csv(lolol +".csv", encoding='utf-8', index=False)
 