import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
r = requests.get(url, headers=headers)
print(r)
soup = BeautifulSoup(r.text, "lxml")
Product_url=[]
Product_name=[]
Product_price=[]
Product_rating=[]
Product_reviews=[]

try:
  def Extraction(soup):
      #Extraction of product name 
      name=soup.find_all("h2",class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2")
      for i in name:
          n=i.text
          Product_name.append(n)
  
      #extraction of the price
      price=soup.find_all("span",class_="a-offscreen")
      for i in price:
          p=i.text
          Product_price.append(p)
     
      #extraction of the rating
      rating=soup.find_all("span",class_="a-icon-alt")
      for i in rating:
          ra=i.text
          if ra != 'null':
              Product_rating.append(ra)
          else:
              Product_rating.append('NA')
     
  
      #extraction of the review
      reviews=soup.find_all("span",class_="a-size-base s-underline-text")
      for i in reviews:
          re=i.text
          if re != 'null':
              Product_reviews.append(re)
          else:
              Product_reviwes.append('NA')
  
      #extraction of the url
      url=soup.find_all("a",class_="a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal")
      product_urls = [link['href'] for link in url]
      for i in product_urls:
          u='https://www.amazon.in' + i
          Product_url.append(u)
      
  
  Extraction(soup)# first page extraction
  
  while True:
    np = soup.find("a", class_='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator').get('href')
    cnp = 'https://www.amazon.in' + np
    url = cnp
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    Extraction(soup)
except AttributeError:
  pass

else:
  #data storing
  df=pd.Dataframe({"ProductName":Product_name , "ProductPrice":Product_price, "ProductRating":Product_rating, "ProductReviews":Product_reviews,"ProductPrice":Product_url})
  df.to_csv("PageData.csv")
  print("Sucsseful")
