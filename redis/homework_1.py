import requests

param = {'date':  "1996-12-24"}
link = "https://api.nasa.gov/planetary/apod?api_key=NNKOjkoul8n1CH18TWA9gwngW1s1SmjESPjNoUFo"
#demo = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

r = requests.get(link, params = param)
data = r.json()
image = data['url']

print(image) 
