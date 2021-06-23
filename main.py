import time
from selenium import webdriver
import os
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import datetime
from random import randint
import json
from pymongo import MongoClient
import re
from bson import ObjectId
from pprint import pprint
site = 'https://www.terabyteshop.com.br/'
# termo_pesquisa = 'Memoria RAM 8gb'
client = MongoClient('mongodb://127.0.0.1:27017/medescavator')
termo_pesquisa = input('Termo de pesquisa:')
estabelecimento = input('Estabelecimento:')
n_produt = int(input('Quantidade de produtos:'))

db=client.medescavator

n_pgs = 1

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
p = 0
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
  preco = 0
  try:
    preco = nav.find_element_by_id('valVista')
  except NoSuchElementException:
    alternativePreco = nav.find_element_by_class_name('p3')
    preco = alternativePreco.find_element_by_tag_name('span')
    pass
  if p == 0:
    try:
      button = WebDriverWait(nav, 10).until(ec.visibility_of_element_located((By.ID,'btnCloseCookie'))).click()
    except TimeoutException:
      pass
  time.sleep(1)
  element = nav.find_elements_by_class_name('panel-group')
  element[2].click()
  time.sleep(1)
  title = nav.find_element_by_class_name('tit-prod')
  tecnica = nav.find_element_by_class_name('tecnicas')
  esptecnica = tecnica.find_elements_by_tag_name('p')
  obj = {}
  obj['nome'] = title.text
  a_string = preco.text
  a_string = a_string.replace(',',"")
  obj['preco'] = int(re.search(r'\d+', a_string).group()) / 100
  for f in esptecnica:
    split = f.text.split(':')
    nome = split[0].replace('\r', '').replace('\n', '').lower()
    value = split[1].replace('\r', '').replace('\n', '').lower()
    obj[nome] = value
  finalObj = {
    'nome':obj['nome'],
    'fabricante':obj['marca'],
    'modelo':obj['modelo'],
    'preco':obj['preco'],
    'status':True,
    'estabelecimento':ObjectId(estabelecimento),
    'descricao':tecnica.get_attribute("innerHTML"),
    'categorias':[ObjectId('60c8d0768089d00569cde3d8')]
  }
  db.produtoCollection.insert_one(finalObj)
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
