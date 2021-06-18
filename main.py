import time
from selenium import webdriver
import os
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json
site = 'https://www.terabyteshop.com.br/'
# termo_pesquisa = 'Memoria RAM 8gb'
termo_pesquisa = 'Placa de vídeo'

n_pgs = 1  # Número de páginas a serem lidas
n_produt = 1
# Configurando o webdriver e inserindo o termo de busca (Memória RAM 8gb)
# firefox_profile = webdriver.FirefoxProfile()
# firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

nav = webdriver.Firefox(executable_path=os.path.join(sys.path[0], "geckodriver"))
nav.get(site)
campo_busca = WebDriverWait(nav, 10).until(ec.visibility_of_element_located((By.ID, 'isearch')))
#nav.find_element_by_id('misearch')
campo_busca.send_keys(termo_pesquisa)
campo_busca.send_keys(Keys.ENTER)

# Aguarda 1 segundo para completar o carregamento
time.sleep(3)

# Cada atributo será armazenado numa lista correspondente


# Inicia o loop de cada página
p = 1
# while True:
#     try:
print(f"Lendo página {p}...")
html = nav.find_element_by_id("prodarea")

html = html.get_attribute("innerHTML")

sopa = BeautifulSoup(html, 'lxml')
#print('item count',len(sopa.find_all('div', {'class': 'commerce_columns_item_inner'})))
for i in sopa.find_all('div', {'class': 'commerce_columns_item_inner'}):
  url = i.find('a', {'class': 'prod-name'}).attrs['href']
  nav.get(url)
  try:
    preco = nav.find_element_by_id('valVista')
  except NoSuchElementException:
    alternativePreco = nav.find_element_by_class_name('p3')
    preco = alternativePreco.find_element_by_tag_name('span')
    pass
  try:
    button = WebDriverWait(nav, 10).until(ec.visibility_of_element_located((By.ID,'btnCloseCookie'))).click()
  except NoSuchElementException:
    pass
  time.sleep(1)
  element = nav.find_elements_by_class_name('panel-group')
  element[2].click()
  time.sleep(1)

  tecnica = nav.find_element_by_class_name('tecnicas')
  esptecnica = tecnica.find_elements_by_tag_name('p')
  print('tenicas',len(esptecnica))
  for f in esptecnica:
    # print(f.text)
    split = f.text.split(':')
    print(split[0].strip(),split[1].strip())
    #if split is not None:
     #if split[1] is not None:
      #print(split[0],split[1],index)
  if p == n_produt:
    print("Extração concluída.")
    break
  p += 1
  #   x = {"name":"teste"}
  #  // print(x['name'])
      # elif f.find_element_by_tag_name('p') is not None:
      #   item = f.find_element_by_tag_name('p')
      #   print(desc.text + " : " + item  + "\n")


    #print('esp',item.find('strong').text)
# nav.close()
