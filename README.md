# WebScraper Testes SARS-Cov-1 por Estado - Webscrapper Brazil SARS-Cov-1 Tests by State

##### Esse código foi implementado em 25 de agosto de 2020, mudancas no front do site podem comprometer o funcionamento do código.
##### This code was implemented on August 25, 2020, changes in the front of the site may compromise the code's functioning.

O Ministério da Saúde disponibiliza hoje em sua [Plataforma Integrada de Vigilância em Saúde](http://plataforma.saude.gov.br/coronavirus/virus-respiratorios/) os dados de testagem SARS-Cov-2 dos estados brasileiros. O nível de testagem de um estado é uma variável improtante para determinar o quanto de controle ele tem sobre como a doença está disseminada em sua população. Esta plataforma contém os dados sobre testes RT-PCR realizados em todos os estados até hoje, porém esssa informacão só está disponivel no na interface e não via API, por isso é importante a raspagem de dados. A coleta de dados web, ou raspagem web, é uma forma de mineração que permite a extração de dados de sites da web convertendo-os em informação estruturada para posterior análise, esse script então realiza a raspagem dos dados de exames por estado.

The Brazilian Ministry of Health makes available, on its [Integrated Health Surveillance Platform](http://plataforma.saude.gov.br/coronavirus/virus-respiratorios/), the SARS-Cov-2 testing data of the Brazilian states. A state's level of testing is an important variable in determining how much control it has over how the disease is spread in its population. This platform contains data on RT-PCR tests carried out in all states to date, however this information is only available on the interface and not via API, so data scraping is important. The collection of web data, or web scraping, is a form of mining that allows the extraction of data from web sites, converting them into structured information for later analysis, this script then scrapes exam data by state.

## CODE

O código está esquematizado para rodar no [Repl.it](https://repl.it/), o selenium e se utiliza do webdriver que é uma ferramenta de código aberto para teste automatizado de aplicativos da web em vários navegadores, especificamente o ChromeDriver é um servidor autônomo que implementa o padrão W3C WebDriver.
```
driver = webdriver.Chrome(options=chrome_options)
```

A funcão principal (main) passa a url do site da plataforma onde o driver irá ser executado. A funcao get navega até o elemento passado.
```
driver.get(url)
src = driver.find_element_by_tag_name("iframe").get_attribute("src")
driver.get(src)
```

A funcao find_elements retorna um vetor de todos os elementos que correspodem a requisicão passada. A funcao click então executa o click como em uma navegacao normal até o elemento indicado. O sleep aguardo o período especificado em segundos antes de executar a próxima acão.
```
element = driver.find_elements_by_xpath("//*[contains(text(), 'Inspect')]")
element[0].click()
sleep(3)
```

Após finalmente chegar até a tabela onde os dados estão disponibilizados, em um DataFrame (df), anteriormente criado, o driver aloca os elementos da tabela, que sào extraidos do HTML, com BeautifulSoup, um pacote Python para análise de documentos HTML e XML.

```
df = pd.DataFrame(columns=['UF', 'Resultados', 'exames'])
for j in range(0, len(tableRows)):
      html = tableRows[j].get_attribute("innerHTML")
      soup = BeautifulSoup(html, "html.parser")
      x = soup.select("td")
      df.loc[i] = [x[0].text, x[1].text, x[2].text]
      i = i+1    
```


Se quiser encontrar o percentual por Estado pode se criar um DataFrame auxiliar e depois fundir os DataFrames.

```
dftotal = df.groupby(['UF']).agg({"exames": "sum"})
dftotal.rename(columns={'exames': 'total'}, inplace=True)
df = df.merge(dftotal, on=['UF'], sort=True, how='left')
df = df[df['Resultados'] == 'Positivo / Detectável']
df['Percentual'] = round((df['exames']/df['total'])*100, 2)
```
