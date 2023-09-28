from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from threading import Thread
import queue

def get_prices_from_carrefour(results, products):
    s=Service(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(f"https://www.carrefour.es/")
    time.sleep(2)
    cookies_btn = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    cookies_btn.click()
    # Obtenemos la barra de busqueda
    search_box = driver.find_element(By.XPATH, '//*[@id="search-input"]')
    search_box.click()
    for p in products:
        search_box2 = driver.find_element(By.XPATH, '//*[@id="empathy-x"]/header/div[1]/div/input[3]')
        # Limpiamos
        search_box2.send_keys(Keys.CONTROL + "a")
        search_box2.send_keys(Keys.DELETE)
        time.sleep(1)
        search_box2.send_keys(p) # Enviamos el nombre del producto
        time.sleep(2)
        search_box.send_keys(Keys.RETURN) # Buscamos
        # Buscamos el precio del primer resultado
        try:
            price = driver.find_element(By.XPATH, '//*[@id="ebx-grid"]/article[1]/div/p/strong')
            # Lo refactorizamos de string a float
            formatted_price = float(price.text.split(" ")[0].replace(",", "."))
            results["carrefour"].append(formatted_price)

        except:
            results["carrefour"].append(0)
    driver.quit()
    return results

# No funciona temporalmente debido a que la web ha cerrado este acceso
def get_prices_from_mercadona(results, products):
    s=Service(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(f"https://lolamarket.com/es/es/tienda/mercadona/")
    time.sleep(1)
    
    # Obtenemos la barra de busqueda
    for p in products:
        try:
            not_available = driver.find_element(By.XPATH, '//*[@id="popoversRoot"]/div/div[2]/button')
            not_available.click()
            search_box = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/header/div[3]/div[1]/form/input')
            # Limpiamos
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.DELETE)
            time.sleep(1)
            search_box.send_keys(p) # Enviamos el nombre del producto
            time.sleep(2)
            search_box.send_keys(Keys.RETURN) # Buscamos
            time.sleep(1)
            # Buscamos el precio del primer resultado
            
            price = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div/div/div/section[1]/div[2]/li[1]/a/div/p/strong")
            # Lo refactorizamos de string a float
            formatted_price = float(price.text.split(" ")[0].replace(",", "."))
            results["mercadona"].append(formatted_price)
        except:
            results["mercadona"].append(0)
    driver.quit()
    return results

def get_prices_from_dia(results, products):
    s=Service(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(f"https://www.dia.es/compra-online/")
    time.sleep(2)
    cookies_btn = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    cookies_btn.click()
    # Obtenemos la barra de busqueda
    for p in products:
        try:
            search_box = driver.find_element(By.XPATH, '//*[@id="search"]')
            search_box.click()
            # Limpiamos
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.DELETE)
            time.sleep(1)
            search_box.send_keys(p) # Enviamos el nombre del producto
            time.sleep(2)
            search_box.send_keys(Keys.RETURN) # Buscamos
            time.sleep(2)
            # Buscamos el precio del primer resultado
            
            price = driver.find_element(By.XPATH, '//*[@id="productgridcontainer"]/div[1]/div[1]/div/a/div[2]/div/p[1]')
            # Lo refactorizamos de string a float
            formatted_price = 0
            if len(price.text.split(" ")) <= 1:
                formatted_price = float(price.text.split("€")[0].replace(",", "."))
            else:
                formatted_price = float(price.text.split(" ")[0].replace(",", "."))
            results["dia"].append(formatted_price)
        except:
            results["dia"].append(0)
    driver.quit()
    return results

def get_prices_from_markets(products):
    # results = {"mercadona": [], "carrefour": [], "dia": []}
    results = {"carrefour": [], "dia": []}
    T1 = Thread(target = get_prices_from_dia, args=(results, products,))
    T2 = Thread(target = get_prices_from_carrefour, args=(results, products,))
    #T3 = Thread(target = get_prices_from_mercadona, args=(results, products,))
    T1.daemon = True
    T2.daemon = True
    #T3.daemon = True
    T1.start()
    T2.start()
    #T3.start()
    T1.join()
    T2.join()
    #T3.join()
    print(results)
    return results