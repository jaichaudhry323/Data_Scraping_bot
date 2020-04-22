

def error(s):
    if str(s)=="None" or len(s)==0:
        return 1
    else:
        return 0

def clean(s):
    s=s.strip()
    s=s.replace("\n"," ")
    s=s.replace(","," ")
    return s

dontscrap=0
test=0
test_limit=10
cnt=0

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bsoup

my_url='https://forum.ge/?s=989cb85ec94736224d89a77e47c5d274&act=idx'
print("Provide the main link")
#my_url=input()

print("Enter Table N.O , 0 or 1 or 2")
tablenum=input()
tablenum=int(tablenum)

uClient=uReq(my_url)
page_html = uClient.read()
uClient.close()

soup = bsoup(page_html,"html.parser")
tables=soup.findAll("div",{"class","tableborder"})

link_f=open("C://Users//Jai//Desktop//links"+str(tablenum)+".csv","w",encoding='utf-8')
link_f.write("links scraped\n")
file=open("C://Users//Jai//Desktop//scrap"+str(tablenum)+".csv","w",encoding='utf-8')
headers="link_name,Topicname,thread_author,views,post_author,date,posttext\n"
file.write(headers)

my_cnt=-1
links_set=set()

print("NUMBER OF TABLES",len(tables))

for tt in tables:

	my_cnt+=1
	if my_cnt!=tablenum:
		continue

	mini_tables=tables[tablenum].findAll("td",{"class":"row4"})
	if my_cnt>3:
		break

	for table in mini_tables:
		
		links=table.find_all("a",href=True)
		for j in links:
			try:
				link_name=j.text.strip()
				link_name=clean(link_name)
				base_url=j['href']
				print("link_name=",link_name,"BASE_URL=",base_url)


				if dontscrap:
					continue




				uClient=uReq(base_url)
				page_html = uClient.read()
				uClient.close()

				soup = bsoup(page_html,"html.parser")

				##################################
				headings=soup.findAll("td",{"nowrap":"nowrap"})

				# print(headings[len(headings)-1].text.strip())  # gives number of pages after including this page
				# headings =  Pages: (24)  [1]  2  3  ...  Last »   ( Go to first unread post ) 
				nn=0
				if str(headings)!="None"  and len(headings)>0:
				    s=headings[len(headings)-1].text.strip()
				    try:
				        s=s[s.find("(")+1:s.find(")")]
				        #print(s)
				        nn=int(s)      # number of pages to be scraped i=1 to n-1 add  i*15 to url
				    except:
				        pass
				print("NUMBER OF PAGES WITH LINKS:",nn,"\n")

				#######################################

				for i in range(nn):
				    try:
				        # PAGE LINK TRAVERSAL
				        print("SCRAPING PAGE WITH POST LINKS : ",i+1)

				        new_url=base_url+"&st="+str(i*40)

				        uClient=uReq(base_url+"&st="+str(i*40))
				        page_html = uClient.read()
				        uClient.close()

				        soup = bsoup(page_html,"html.parser")

				        ###################################

				        # get main title
				        main="None"
				        main=soup.find("div",{"class":"maintitle"})
				        if main!="None":
				            main=main.text.strip()
				            maintopic=str(main)

				        tables=soup.findAll("div",{"class":"tableborder"})

				        rows=""
				        for table in tables:
				            mt=table.find("div",{"class":"maintitle"})
				            if str(mt)!="None":
				                # get all rows with the links
				                rows=table.findAll("tr")
				                print("TOTAL ROWS=",len(rows))

				        # pick a row of topic
				        count=0
				        for row in rows:
				            if count==0:   # first link got taken twice hence added this
				                count+=1
				                continue

				            thread_author=""
				            views=""
				            link=""
				            topicname=""
				        #row=row[8]
				            if row!="None" and len(row)>0:
				                
				                linkboxes=row.findAll("td",{"class":"row4"})

				                linkboxdata=[]

				                if error(linkboxes):
				                    #print("\nERROR\n")
				                    continue
				                
				                for i in linkboxes:
				                    linkboxdata.append(i.text.strip())

				                # topicname     
				                topicname=linkboxdata[1].split("(")[0]

				                ##############################
				                link=""

				                links=row.find_all("a",href=True,title=True)

				                if str(links)=="None" or len(links)==0:
				                    continue
				                link=links[0]['href']
				                ######################################
				                
				                if len(linkboxdata)>=5:    
				                    # # topicname     
				                    # topicname=linkboxdata[1].split("(")[0]
				                    print("D")
				                    # Thread author
				                    thread_author=linkboxdata[2]
				                    # views 
				                    views=linkboxdata[4]

				                    # print("topicname:",topicname," thread_author",thread_author," views",views)
				                    # print("\n")
				                else:
				                    print("L")

				                    linkboxes2=row.findAll("td",{"class":"row2"})

				                    if error(linkboxes2):
				                        #print("\nERROR\n")
				                        continue

				                    thread_author=linkboxes2[1].text.strip()

				                    views=linkboxes2[2].text.strip()
				                # print(maintopic)

				                topicname=topicname.strip()
				                thread_author=thread_author.strip()

				                topicname=clean(topicname)
				                thread_author=clean(thread_author)
				                views=clean(views)
				                cnt+=1
				                
				                if test and cnt>test_limit:
				                            break
				                        
				                print("topicname:",topicname," thread_author",thread_author," views",views,"\nlink",link,"\n")

				                # NOW THE LINK NEED TO BE SCRAPED 




				                my_url=link

				                if link in links_set:
				                	print("DUPLICATE LINK")
				                	continue
			                	
			                	print("WRITING TO LINK_F")

			                	links_set.add(link)
			                	link_f.write(link+"\n")
			                	



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

				                                        file.write(link_name+","+topicname+","+thread_author+","+views+","+u+","+d+","+p+"\n")
				                    
				                    except:
				                        #pass
				                        continue
				    except:
				        continue



			except:
				print("exception with main page link")
				pass


print("CLOSING FILE")
file.close()
link_f.close()