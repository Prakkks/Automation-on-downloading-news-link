import os
import time #introduces delay
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# make documentation of each project we have done

def job():  
    #Set the full path for download directory
    download_directory = os.path.join(os.getcwd(),'gorkhapatrafriday') #search directory

    #create the directory if not existing 
    if not os.path.exists(download_directory):
        os.makedirs(download_directory) #create directory

      