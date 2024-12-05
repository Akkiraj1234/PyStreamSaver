import sys
sys.path.append("..\\src")

from streamdl.StreamScraper import Scraper
from streamdl.youtubedl import YouTube

link = "https://youtu.be/yQdQ4HTEdI4?si=utIFgBo_DpriH_MB"
with Scraper(link) as scraper:
    data = scraper._getting_data(scraper.data, "ytInitialPlayerResponse")
    
    data = YouTube(data)
    
    print(data.title())
    print(data.get_streaming_data())
    

