from proxy import * 
import time
import undetected_chromedriver as UC
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys 
from selenium.webdriver.common.action_chains import ActionChains

RUTA_CHROMEDRIVER = ""
login_url = 'https://www.myexternalip.com/raw'
username = ' '

password =  ' '
def main():
    # temp =  "./proxies"
    # proxy_scrape()
     
    
    # proxies = open(temp).read().split('\n')
    # proxy = proxies[0]
    
    browser = UC.Chrome(driver_executable_path=RUTA_CHROMEDRIVER, headless=False)
    browser.get(login_url)
    
    time.sleep(5)
    input_credenciales = browser.find_element(By.NAME, 'login[username]')
    input_credenciales.send_keys(username)
    time.sleep(4)
    boton_next = browser.find_element(By.ID, 'login_password_continue')
    # boton_next.click()
    action = ActionChains(browser)
    action.pause(4).move_to_element(boton_next).pause(1).click().perform()

    time.sleep(7)
    # browser.save_screenshot('./debug.png')
    input_password = browser.find_element(By.NAME, 'login[password]')
    input_password.send_keys( password)

    boton_next = browser.find_element(By.ID, 'login_control_continue')
    # boton_next.click()

    action = ActionChains(browser)
    action.pause(4).move_to_element(boton_next).pause(2).click().perform()


    time.sleep(7)

if __name__ == "__main__":
    try:

        main()
    except:
        time.sleep(1000)    