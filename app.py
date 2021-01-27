from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def fix_exames(row):
    x = row['exames'].replace('.', '')
    return x

def raspagem(url):
  i = 0
  df = pd.DataFrame(columns=['UF', 'Resultados', 'exames'])
  # No Repl.it
  driver = webdriver.Chrome(options=chrome_options)
  # Caso seja local
  # driver = webdriver.Chrome(options=chrome_options, executable_path='C:/Users/User/Documents/IMPULSO/chromedriver.exe')
  driver.get(url)
  src = driver.find_element_by_tag_name("iframe").get_attribute("src")
  driver.get(src)
  sleep(40)
  element = driver.find_elements_by_class_name("dshPanel__headerButtonGroup")
  try:
    while len(element) < 11:
      sleep(15)
      element = driver.find_elements_by_class_name("dshPanel__headerButtonGroup")
    sleep(25)
    element[11].click()
    sleep(3)
    element = driver.find_elements_by_xpath("//*[contains(text(), 'Inspect')]")
    element[0].click()
    sleep(3)
    element = driver.find_elements_by_xpath("//*[contains(text(), 'Rows')]")
    element[0].click()
    sleep(3)
    element = driver.find_elements_by_xpath("//*[contains(text(), '50 rows')]")
    element[0].click()
    sleep(3)
    tableRows = driver.find_elements_by_class_name("euiTableRow")
    for j in range(0, len(tableRows)):
      html = tableRows[j].get_attribute("innerHTML")
      soup = BeautifulSoup(html, "html.parser")
      x = soup.select("td")
      df.loc[i] = [x[0].text, x[1].text, x[2].text]
      i = i+1    
    element = driver.find_elements_by_class_name("euiPagination")
    element[0].click()
    sleep(5)
    tableRows = driver.find_elements_by_class_name("euiTableRow")
    for j in range(0, len(tableRows)):
      html = tableRows[j].get_attribute("innerHTML")
      soup = BeautifulSoup(html, "html.parser")
      x = soup.select("td")
      df.loc[i] = [x[0].text, x[1].text, x[2].text]
      i = i+1    
    return df
  except:
    print("""
    O carregamento falhou ou demorou demais, por favor tente novamente.
    """)
    return df

  
df = raspagem('http://plataforma.saude.gov.br/coronavirus/virus-respiratorios/')
df['exames'] = df.apply(fix_exames, axis=1).astype(int)
dftotal = df.groupby(['UF']).agg({"exames": "sum"})
dftotal.rename(columns={'exames': 'total'}, inplace=True)
df = df.merge(dftotal, on=['UF'], sort=True, how='left')
df = df[df['Resultados'] == 'Positivo / Detectável']
df['Percentual'] = round((df['exames']/df['total'])*100, 2)
df.drop(['Resultados','exames','total'], axis=1, inplace=True)
if len(df) > 0:
  print("""
  Abaixo segue dados de Dataframe com o Percentual de resultados Positivo/Detectável por Quantidade de Exame Realizado em cada Estado.

  """)
  print(df.to_string())
#Para caso queira um csv
#df.to_csv("dataframe.csv")
