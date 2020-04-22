# WORKS FOR THE HEAVY TOPIC BASED PAGE , ALL LINKS FROM ALL CONNECTED PAGES, the one with the links to post pages

# LINK TRANSFORMATION REQUIRED

# https://forum.ge/?showtopic=35127640&f=&st=0&#entry55535380
# to
# https://forum.ge/?f=59&showtopic=35127640

########################

# the link that i got from scraping , puttinh &st=15*i i=1->num of pages-1 works
# https://forum.ge/?s=d84ecab77f76b865d258c2be0227cd6c&f=59&showtopic=35127640

#----MADE FROM---#
# https://forum.ge/?showforum=59

test=0
test_limit=3
cnt=0

def error(s):
    if str(s)=="None" or len(s)==0:
        return 1
    else:
        return 0

def clean(s):
    s=s.strip()
    s=s.replace("\n"," ")
    return s


from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bsoup

base_url='https://forum.ge/?showforum=73'
print("enter the url containing links to posts u wanna scrape")
base_url=input()

uClient=uReq(base_url)
page_html = uClient.read()
uClient.close()

soup = bsoup(page_html,"html.parser")


####################################################3
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
###################################################3

for i in range(nn):
    try:
        # PAGE LINK TRAVERSAL
        print("SCRAPING PAGE WITH POST LINKS : ",i+1)
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

    except:
        continue

