import requests
from bs4 import BeautifulSoup
import re
import cssutils


lines_seen = set() # holds lines already seen
outfile = open('outfilename', "w")
for line in open('pic_urls.txt', "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()





'''
with open('pic_urls.txt', mode='r') as infile:
  htmlstr = infile.read()
  result = 'str'
  while result!=[]:
    result = re.search("style='background-image: url(.*)'></div>", htmlstr)
    if result == None:
      break
    tmp = result.group(1)
    keystr = tmp
    outputstr.append(keystr)
    htmlstr = htmlstr.split(tmp)[1]
    if htmlstr ==[]:
      break


with open('out_.txt', mode='w') as outfile:
  for i in outputstr:
    a = i[1:]
    b = a[:-1]
    outfile.write(b+'\n')



htmlContent = requests.get('https://www.pexels.com/search/girl')
soup = BeautifulSoup(htmlContent.text, 'html.parser')
print(soup.find_all("div", class_="image-tag__img"))
quit()

with open('filepath', mode='w') as outfile:
  div_style = soup.findAll('div', attrs={'class': 'image-tag__img'})
  print (div_style)
  #div_style = soup.find('div')['style']
  style = cssutils.parseStyle(div_style)
  url = style['background-image']
  
  outfile.write(url)

'''