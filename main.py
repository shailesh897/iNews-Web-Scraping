from flask import Flask,render_template
app = Flask(__name__)


@app.route('/')
def index():
    import csv
    path_for_csv='''C:\\Users\\hp\\Documents\\Coding\\WebScrapingIneuron\\scrapped_news.csv'''
    with open(path_for_csv) as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        news_list = []
        for row in data:
            if not first_line:
                news_list.append({
                "heading": row[0],
                "content": row[1]
                })
            else:
                first_line = False
    return render_template("index.html", news_list=news_list)

def scrape_data():
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
 
    link="""https://www.ndtv.com/latest?pfrom=home-ndtv_mainnavgation"""
    html_text=requests.get(link).text

    soup=BeautifulSoup(html_text,'lxml')
    blocks=soup.find_all('div',class_='news_Itm-cont')

    heading_list=[]
    para_list=[]
    
    for block in blocks:
        heading=block.find('a').text
        heading_list.append(heading)
        print(heading,end='--\n')
    
        para=block.find('p',class_='newsCont').text
        para_list.append(para)
        print(para,end="\n\n\n")

    df = pd.DataFrame({'Heading':heading_list,'Paragraph':para_list}) 
    df.to_csv('scrapped_news.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    scrape_data()
    app.run(debug=True)