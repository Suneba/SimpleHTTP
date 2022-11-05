import webbrowser
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyngrok import ngrok, conf

def get_the_url():
    ngrok.get_ngrok_process()

def File_checker_at_Boot_and_Creator():
    conf._default_pyngrok_config

def Browse_Folder():
    pass

def start():

    ngrok_process = ngrok.get_ngrok_process()
    ngrok.connect(80)
    try:
        # Block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print(" Shutting down server.")

        ngrok.kill()

def stop():
    ngrok.kill()

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
    return x
