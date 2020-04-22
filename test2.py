# WORKS PERFECTLY FOR ALL PAGES OF POSTS LINKED TOGETHER

# https://forum.ge/?f=36&showtopic=33692599
# https://forum.ge/?f=59&showtopic=33616434

# post_author=username

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bsoup

file=open("C://Users//Jai//Desktop//test.csv","w",encoding='utf-8')
headers="post_author,date,posttext\n"
file.write(headers)
my_url='https://forum.ge/?f=36&showtopic=33692599'
print("Provide a link which has posts")
my_url=input()

uClient=uReq(my_url)
page_html = uClient.read()
uClient.close()

soup = bsoup(page_html,"html.parser")

#posts=soup.findAll("div",{"class":"postcolor"})

###############################

headings=soup.findAll("td",{"nowrap":"nowrap"})

# print(headings[len(headings)-1].text.strip())  # gives number of pages after including this page
# headings =  Pages: (24)  [1]  2  3  ...  Last »   ( Go to first unread post )	
n=0
if str(headings)!="None"  and len(headings)>0:
	s=headings[len(headings)-1].text.strip()
	try:
		s=s[s.find("(")+1:s.find(")")]
		#print(s)
		n=int(s)      # number of pages to be scraped i=1 to n-1 add  i*15 to url
	except:
		pass
print("NUMBER OF PAGES:",n,"\n")

for i in range(n):
	try:
		print("SCRAPING PAGE : ",i+1)
		uClient=uReq(my_url+"&st="+str(i*15))
		page_html = uClient.read()
		uClient.close()

		soup = bsoup(page_html,"html.parser")

		#############
		tables=soup.findAll("div",{"class":"tableborder"})

		for table in tables:
			
			# table=tables[0]
			if len(table)>0:
				
				boxes=table.findAll("table")

				if str(boxes)!="None" and len(boxes)>0:
					for box in boxes:
						# box=boxes[1]

						username=box.find("span",{"class":"normalname"})
						if str(username)=="None":
							continue
						username=username.text.strip()

						posttexts=box.findAll("div",{"class":"postcolor"})
						if str(posttexts)=="None" or len(posttexts)==0:
							continue
						posttext=""
						for pt in posttexts:
							posttext+=pt.text.strip()

						# date
						textboxes=box.findAll("td")
						if str(textboxes)=="None" or len(textboxes)<=1:
							continue
						date=(textboxes[1]).text.strip().split(":")[1].split(",")[0]

						quote=""
						quotes=box.findAll("td",{"id":"QUOTE"})
						if str(quotes)=="None" or len(quotes)==0:
							lol=1
						else:
							for q in quotes:
								p=q.text.strip()
								posttext+=" "+p
								quote+=" "+p

						print("\nusername:",username,"\nposttext:",posttext,"\ndate:",date,"\nquote",quote,"\n")
						u=username.replace(","," ")
						u=u.replace("\n"," ")
						d=date.replace(","," ")
						d=d.replace("\n"," ")
						p=posttext.replace(","," ")
						p=p.replace("\n"," ")

						file.write(u+","+d+","+p+"\n")
	
	except:
		continue

print("CLOSING FILE")
file.close()