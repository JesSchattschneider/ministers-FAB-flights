import requests
from bs4 import BeautifulSoup
import urllib.request
# ref: https://jonathansoma.com/lede/foundations/classes/friday%20sessions/advanced-scraping-form-submissions-completed/
# todo : save pdfs to ./pdfs folder. Create folder if it doesn't exist.

years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
URL = "https://www.fab.mil.br/voos/index"
for year in years:

    # post parms
    post_params = {"VoosForm[ano]": year}
    page = requests.post(URL, data=post_params)
    
    # parse html
    soup = BeautifulSoup(page.content, "html.parser")

    # find id
    results = soup.find(id="portal-column-content")

    # in the id find all links
    for link in results.find_all('a'):
        current_link = link.get('href')
        if current_link.endswith('pdf'):
            print(current_link)
            response = urllib.request.urlopen(current_link)    
            file = open(str(current_link).replace("https://www.fab.mil.br/cabine/voos/", "", 1), 'wb')
            file.write(response.read())
            file.close()