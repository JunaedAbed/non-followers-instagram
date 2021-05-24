from selenium import webdriver
from time import sleep
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = 'junaedccpc17@gmail.com'
EMAIL_PASS = '####'

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome(executable_path='C:/Users/junae/Downloads/chromedriver.exe')
        self.username = username
        self.driver.get('https://www.instagram.com/')
        sleep(2)
        self.driver.find_element_by_xpath('//input[@name=\"username\"]')\
            .send_keys(username)
        self.driver.find_element_by_xpath('//input[@name=\"password\"]')\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]')\
            .click()
        sleep(2)
        
    def get_unfollowers(self):
        self.driver.find_element_by_xpath('//a[contains(@href, "/{}")]'.format(self.username))\
            .click()
        sleep(3)
        self.driver.find_element_by_xpath('//a[contains(@href, "/{}/following")]'.format(self.username))\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath('//a[contains(@href, "/{}/followers")]'.format(self.username))\
            .click()
        followers = self._get_names()
        not_following = [user for user in following if user not in followers]
        self._sending_mail(not_following)
        self.driver.quit()
        
    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            sleep(1)
            height = self.driver.execute_script(""" 
                    arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                    return arguments[0].scrollHeight;
                    """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button')\
            .click()
        return names
        
    def _sending_mail(self, list_of_nonfollowers):
        msg = EmailMessage()
        msg['Subject'] = 'List of Non-followers on Instagram!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'junaed98m@gmail.com'
        msg.set_content('list_of_nonfollowers')
        msg.add_alternative(f"""\
            <!DOCTYPE html>
            <html>
            <body>
                <p>List of Names: {', '.join(list_of_nonfollowers)}</p>
            </body>
            </html>
        """, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
            
            smtp.send_message(msg)
        
        
my_bot = InstaBot('mugdho.abed', '#####')
my_bot.get_unfollowers()