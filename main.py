from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def _click_see_more_by_class_name(self, class_name):
    try:
        _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )
        div = self.driver.find_element_by_class_name(class_name)
        div.find_element_by_tag_name("button").click()
    except Exception as e:
        pass 

# text_file = open("output.txt", "w")
 

driver  = webdriver.Chrome(ChromeDriverManager().install())


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

 
#Go to company webpage
browser.get(link)

#elementID.find_element_by_name('posts')
#Simulate scrolling to capture all posts
SCROLL_PAUSE_TIME = 5


# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
 
for i in range(3):
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('Scroll=')
    print(i)
    print('end')
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
   
    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


    
 



 
        duration = None

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    self.__TOP_CARD,
                )
            )
        )
        self.name = root.find_elements_by_xpath("//section/div/div/div/*/li")[0].text.strip()

        # get about
        try:
            see_more = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='lt-line-clamp__more']",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", see_more)

            about = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='lt-line-clamp__raw-line']",
                    )
                )
            )
        except:
            about = None
        if about:
            self.add_about(about.text.strip())

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )

        # get experience
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/5));"
        )

        ## Click SEE MORE
        self._click_see_more_by_class_name("pv-experience-section__see-more")

        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "experience-section"))
            )
            exp = driver.find_element_by_id("experience-section")
        except:
            exp = None

        if exp is not None:
            for position in exp.find_elements_by_class_name("pv-position-entity"):
                position_title = position.find_element_by_tag_name("h3").text.strip()

                try:
                    company = position.find_elements_by_tag_name("p")[1].text.strip()
                    times = str(
                        position.find_elements_by_tag_name("h4")[0]
                        .find_elements_by_tag_name("span")[1]
                        .text.strip()
                    )
                    from_date = " ".join(times.split(" ")[:2])
                    to_date = " ".join(times.split(" ")[3:])
                    duration = (
                        position.find_elements_by_tag_name("h4")[1]
                        .find_elements_by_tag_name("span")[1]
                        .text.strip()
                    )
                    location = (
                        position.find_elements_by_tag_name("h4")[2]
                        .find_elements_by_tag_name("span")[1]
                        .text.strip()
                    )
                except:
                    company = None
                    from_date, to_date, duration, location = (None, None, None, None)

                experience = Experience(
                    position_title=position_title,
                    from_date=from_date,
                    to_date=to_date,
                    duration=duration,
                    location=location,
                )
                experience.institution_name = company
                self.add_experience(experience)

        # get location
        location = driver.find_element_by_class_name(f"{self.__TOP_CARD}--list-bullet")
        location = location.find_element_by_tag_name("li").text
        self.add_location(location)

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

        # get education
        ## Click SEE MORE
        self._click_see_more_by_class_name("pv-education-section__see-more")
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "education-section"))
            )
            edu = driver.find_element_by_id("education-section")
        except:
            edu = None
        if edu:
            for school in edu.find_elements_by_class_name(
                "pv-profile-section__list-item"
            ):
                university = school.find_element_by_class_name(
                    "pv-entity__school-name"
                ).text.strip()

                try:
                    degree = (
                        school.find_element_by_class_name("pv-entity__degree-name")
                        .find_elements_by_tag_name("span")[1]
                        .text.strip()
                    )
                    times = (
                        school.find_element_by_class_name("pv-entity__dates")
                        .find_elements_by_tag_name("span")[1]
                        .text.strip()
                    )
                    from_date, to_date = (times.split(" ")[0], times.split(" ")[2])
                except:
                    degree = None
                    from_date, to_date = (None, None)
                education = Education(
                    from_date=from_date, to_date=to_date, degree=degree
                )
                education.institution_name = university
                self.add_education(education)

        # get interest
        try:

            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            interestContainer = driver.find_element_by_xpath(
                "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']"
            )
            for interestElement in interestContainer.find_elements_by_xpath(
                "//*[@class='pv-interest-entity pv-profile-section__card-item ember-view']"
            ):
                interest = Interest(
                    interestElement.find_element_by_tag_name("h3").text.strip()
                )
                self.add_interest(interest)
        except:
            pass

        # get accomplishment
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            acc = driver.find_element_by_xpath(
                "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']"
            )
            for block in acc.find_elements_by_xpath(
                "//div[@class='pv-accomplishments-block__content break-words']"
            ):
                category = block.find_element_by_tag_name("h3")
                for title in block.find_element_by_tag_name(
                    "ul"
                ).find_elements_by_tag_name("li"):
                    accomplishment = Accomplishment(category.text, title.text)
                    self.add_accomplishment(accomplishment)
        except:
            pass

        # get connections
        try:
            driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mn-connections"))
            )
            connections = driver.find_element_by_class_name("mn-connections")
            if connections is not None:
                for conn in connections.find_elements_by_class_name("mn-connection-card"):
                    anchor = conn.find_element_by_class_name("mn-connection-card__link")
                    url = anchor.get_attribute("href")
                    name = conn.find_element_by_class_name("mn-connection-card__details").find_element_by_class_name("mn-connection-card__name").text.strip()
                    occupation = conn.find_element_by_class_name("mn-connection-card__details").find_element_by_class_name("mn-connection-card__occupation").text.strip()

                    contact = Contact(name=name, occupation=occupation, url=url)
                    self.add_contact(contact)
        except:
            connections = None