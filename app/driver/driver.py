from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from .driver_interface import DriverInterface
from ..files.write_files_interface import WriteFilesInterface
import os , time , pyautogui , inject



class Driver(DriverInterface):
    @inject.autoparams()
    def __init__(self , write_files_interface: WriteFilesInterface):
        self.write_files = write_files_interface
        self.driver = None
    
                
    
    def start_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        service = Service("/usr/local/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    
    

    '''
    0: captcha challenge solved after a few attempts
    1: captcha is inactive
    2: captcha challenge failed to solve
    3: wrong login credentials after 3 attempts. Email sent
    '''
    def login(self) -> int:
        total_attempts = 3
        
        self.is_captcha_active_before_login_credentials()
            
        for _ in range(total_attempts):
            if(self.is_logged_in()):
                return 1
            
            try:
                site_username = os.getenv('site_username')
                site_password = os.getenv('site_password')
                username_input = self.find_input("#input-username")
                username_input.click()
                username_input.clear()
                username_input.send_keys(site_username)
                password_input = self.find_input("#current-password")
                password_input.click()
                password_input.clear()
                password_input.send_keys(site_password)
                log_in_button = self.find_button(By.CSS_SELECTOR , ".submit-btn")
                log_in_button.click()
                
                
                result = self.is_captcha_active_after_login_credentials()
                if(result != 3):    # wrong credentials, try again
                    return result
                    
            except Exception as e:
                print(f'An error occured trying to logging in: {str(e)}')
                self.write_files.write_total_errors()
               
                
        return 3    # wrong credentials




    def logout(self) -> None:
        if(not self.is_logged_in()):
            return

        try:
            WebDriverWait(self.driver , 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR ,"a[href='/account']"))).click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/logout/']"))).click()
        
        except Exception as e:
            print(f'An error occured trying to logging out: {str(e)}')
            self.write_files.write_total_errors()
    

    
    
    def wrong_credentials_in_login(self) -> bool:
        try:
            WebDriverWait(self.driver , 10).until(EC.visibility_of_element_located((By.XPATH ,
            "//div[contains(. , 'Λάθος όνομα χρήστη ή κωδικός')]"
            )))

            return True
            
        except TimeoutException:
            self.write_files.write_total_errors()
            return False

        
    
    
    
    
    def accept_cookies(self) -> bool:
        if not self.has_cookies_popup():
            return False

        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "accept-btn"))
            )
            button.click()
            return True
        
        except TimeoutException:
            self.write_files.write_total_errors()
            return False







    def update_machine(self , url_link: str) -> bool:
        try:
            self.open_url(url_link)
            return self.update()

        except Exception as e:
            print(f'An error occured updating a machine: {str(e)}')
            self.write_files.write_total_errors()
    
    



    def open_url(self ,url: str) -> None:
        try:
            self.driver.get(url)

        except Exception as e:
            print(f'An error occured opening url: {str(e)}')
            self.write_files.write_total_errors()
        






    def update(self) -> bool:
        xpath = (
                    "//button[.//span[contains(@class,'tw-max-w-full') and "
                    "(normalize-space()='Ανανέωση' or normalize-space()='Ανανεώθηκε')]]"
                )

        try:    
            button = WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.XPATH , xpath)))
            button.click()
            state_span = button.find_element(By.XPATH, ".//span[contains(@class,'tw-max-w-full')]")
            text = state_span.text.strip()

            return text == 'Ανανέωση'

        except TimeoutException as e:
            print(f'No update button found: {str(e)}')
            self.write_files.write_total_errors()

        except Exception as e:
            print(f"An error occured while trying to update: {str(e)}")
            self.write_files.write_total_errors()

            





    def find_input(self, selector) -> None:
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR , selector)))




    def find_button(self , by , value) -> None:
        return WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((by , value)))
    
    
    

    def find_element(self , button_string) -> None:
        return WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR , button_string)))



            
    def has_cookies_popup(self) -> bool:
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "onetrust-banner-sdk")))
            return True
        
        except TimeoutException:
            self.write_files.write_total_errors()
            return False

        




    def is_logged_in(self) -> None:
        # Logged-in users have an avatar image
        elements = self.driver.find_elements(By.CSS_SELECTOR , 'a[href="/account"] img')
        
        return len(elements) > 0
    
    
    
    

    def captcha_challenge_after_login_credentials(self) -> bool:
        try:
            WebDriverWait(self.driver , 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR , ".submit-btn")))
            return False
        
        except TimeoutException:
            self.write_files.write_total_errors()
            return True



    '''
    0: captcha challenge solved after a few attempts
    1: captcha is inactive
    2: captcha challenge failed to solve
    '''
    def is_captcha_active_before_login_credentials(self) -> int:
        if("needs to review the security" in self.driver.page_source.lower()):
            self.write_files.write_number_of_captcha_challenge()
            width , height = pyautogui.size()
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(width / 2 - 345 , height / 2 - 105 , duration=1)
            
            captcha_attempts = 10
            for i in range(captcha_attempts):
                if("needs to review the security" in self.driver.page_source.lower()):
                    pyautogui.click()
                    time.sleep(7)
               
                else:
                    return 0
            
            if("needs to review the security" in self.driver.page_source.lower()):
                return 2
        
        else:
            return 1




    '''
    0: captcha challenge solved after a few attempts
    1: captcha is inactive
    2: captcha challenge failed to solve
    3: wrong credentials
    '''
    def is_captcha_active_after_login_credentials(self) -> int:
        if(self.captcha_challenge_after_login_credentials()):
            self.write_files.write_number_of_captcha_challenge()
            width , height = pyautogui.size()
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(width / 2 - 100 , height / 2 + 60 , duration=1)

            captcha_attempts = 10
            for i in range(captcha_attempts):
                if(self.wrong_credentials_in_login()):
                    return 3

                if(not self.is_logged_in()):
                    pyautogui.click()
                    time.sleep(7)
                    
                else:
                    return 0
            
            if(not self.is_logged_in()):
                return 2
        
        else:
            return 1