import webbrowser
import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
def File_checker_at_Boot_and_Creator():
    pass

def Browse_Folder():
    pass

def start():
    subprocess.call(r"C:\Users\verma\PycharmProjects\pythonProject\ngrok.bat")

def stop():
    subprocess.call(r"C:\Users\verma\PycharmProjects\pythonProject\killngrok.bat")

def Control_Panel():
    webbrowser.open('http://127.0.0.1:4040')

def Get_link():

    PATH = r"C:\Users\verma\PycharmProjects\pythonProject\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("http://127.0.0.1:4040/inspect/http")

    # print(driver.page_source)
    content = driver.find_element(By.CLASS_NAME, 'tunnels')
    x = content.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    # print(content)
    print(x)
