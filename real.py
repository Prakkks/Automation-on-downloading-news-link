import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd 
import numpy as np

def is_social_media(url):
    social_media_domain=['twitter.com','facebook.com','instgram.com']
    for domain in social_media_domain:
        if domain in url:
            return True
    return False

def extract_all_links(url):
    try:
        #send a GET request to the URL
        response = requests.get(url)
        
        #check if the request was successful (status code 200)
        if response.status_code==200:
            #parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = [a['href'] for a in soup.find_all('a', href=True)]
            
            #convert relative URL:half in absolute URL:complete with https
            links=[urljoin(url,link) for link in links]
            
            return links
        
        else:
            print(f"Failed to retrieve data from '{url}' . Status code: {response.status_code}")
            return []
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to URL '{url}': {e}")
        return []
    
def save_links_to_csv(links, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer=csv.writer(csvfile)
        csv_writer.writerow(['Link'])
        
        for link in links:
            csv_writer.writerow([link])
            
def extract_specific_content(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #skip extraction from social media URLs
        if is_social_media(url):
            print(f"Skipping {url} because it's a social media link.")
            return None,None,None,None,None,None,
        
        heading_element=soup.find('h1',{'style':'margin-bottom:0.1rem'})
        author_element=soup.find('h5',class_='text-capitalize')
        publication_date_element=soup.find('div', class_='updated-time')
        content_container=soup.find('div', class_='subscribe--wrapperx')
        
        #Determine category based on URLs
        url_parts=urlparse(url).path.split('/')
        category=next((part for part in url_parts if part),'Category not found')
        
        heading=heading_element.text.strip() if heading_element else 'Heading not found'
        author=author_element.text.strip() if author_element else 'Author not found'
        publication_date_raw=publication_date_element.text.strip() if publication_date_element else 'Date not found'
        publication_date=publication_date_raw.replace('Publised at:','').strip()
        content=content_container.get_text(separator=' ', strip=True) if content_container else 'Content not found'
        
        return heading,author,publication_date,content,url,category
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve content from '{url}'. Error {e}")
        return None,None,None,None,url,None
    
def save_to_csv(data, csv_file_path):
    with open(csv_file_path,'a',newline='',encoding='utf-8') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerows(['Heading','Author','Publication_date','Source','Content','URLs','Category'])
        csv_writer.writerow(data)
        
def main():
    csv_file_path='Kathmandupost.csv'
    with open(csv_file_path,'w',newline='',encoding='utf-8') as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerows(['Heading','Author','Publication_date','Source','Content','URLs','Category'])
        
    url='https://kathmandupost.com'
    links=extract_all_links(url)
    
    #save links to csv_file
    csv_filename='data_links.csv'
    save_links_to_csv(links, csv_filename)
    
    #print message indicating success
    print(f"All links saved to {csv_filename}")
    
    link=pd.read_csv('data_links.csv')
    
    for url in links:
        if not urlparse(url).scheme:
            url=urljoin('https://', url)
            
        if urlparse(url).netloc and not is_social_media(url):
            heading,author,publication_date,content,link,category=extract_specific_content(url)
            if heading is not None and author is not None and content is not None:
                data_to_save=[heading,author,publication_date,'The Kathmandu Post', content,link,category]
                save_to_csv(data_to_save, csv_file_path)
                print(f"Data saved for{url}")
        else:
            print("invalid URL")
        
if __name__=="__main__":
    main()
    
    