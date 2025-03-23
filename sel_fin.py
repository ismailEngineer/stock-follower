from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()

# Ouvrir Google Finance pour l'action Tesla (TSLA)
url = "https://www.google.com/finance/quote/TSLA:NASDAQ"
driver.get(url)

# Gérer la popup des cookies (si elle apparaît)
time.sleep(2)  # Attendre le chargement
try:
    accept_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Tout refuser")]')#Reject all
    accept_button.click()
    print("Cookies acceptés.")
except NoSuchElementException:
    print("Pas de popup de cookies.")


# Attendre le chargement des données
time.sleep(2)

# Extraire le prix actuel de l'action
try:
    price_element = driver.find_element(By.XPATH, '//div[@class="YMlKec fxKbKc"]')
    price = price_element.text
    print(f"Prix actuel de l'action TSLA : {price}")
except NoSuchElementException:
    print("Impossible de récupérer le prix.")

# Extraire le prix actuel de l'action
try:
    price_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "gyFHrc")]')
    # price = price_element.text
    for element in price_elements :
        description = element.find_element(By.XPATH, './/div[contains(@class, "mfs7Fc")]')
        price = element.find_element(By.XPATH, './/div[contains(@class, "P6K39c")]')
        
        print(f" {description.text}: {price.text}")
        #print(f"Prix actuel de l'action TSLA : {element.text}")
except NoSuchElementException:
    print("Impossible de récupérer le prix.")



    

# Fermer le navigateur
driver.quit()
