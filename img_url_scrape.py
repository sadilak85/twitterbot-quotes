import re

outputstr=[]
with open('htmlsource_.txt', mode='r') as infile:
  htmlstr = infile.read()
  result = 'str'
  while result!=[]:
    result = re.search('z_h_9d80b z_h_2f2f0" src="(.*)" alt', htmlstr)
    if result == None:
      break
    print(result.group(1))
    tmp = result.group(1)
    keystr = tmp+'\n'
    outputstr.append(keystr)
    htmlstr = htmlstr.split(tmp)[1]
    if htmlstr ==[]:
      break


with open('out_.txt', mode='w') as outfile:
  for i in outputstr:
    outfile.write(i)


