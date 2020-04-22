# FOR ONE PAGE

# WORKS FOR THE HEAVY TOPIC BASED PAGE, the one with the links to post pages

# LINK TRANSFORMATION REQUIRED

# https://forum.ge/?showtopic=35127640&f=&st=0&#entry55535380
# to
# https://forum.ge/?f=59&showtopic=35127640

########################

# the link that i got from scraping , puttinh &st=15*i i=1->num of pages-1 works
# https://forum.ge/?s=d84ecab77f76b865d258c2be0227cd6c&f=59&showtopic=35127640

#----MADE FROM---#
# https://forum.ge/?showforum=59


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


from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bsoup
import os
import csv
import subprocess as sp   # for linux
#import time

print("1->write to file , 0-> dont write to file")
write_file=0
write_file=int(input())


print_post=1
print_topic=1

clear=1
clear_limit=100

post_count=1

test=0
test_limit=1
cnt=0

print("ENTER TABLE NUMBER 0 or 1 or 2")
tablenum=input()

print("ENTER FILE NUMBER")
filenum=input()


print("SURE U WANNA CREATE THIS FILE ?? 0 or 1")
sure=int(input())
if sure==0:
	exit()

idx="_"+str(tablenum)+"_"+str(filenum)

links_set=set()

#############################################################
###----GETTING PREVIOUSLY SCRAPED LINKS----####

try:
	file2=open("final_links"+idx+".csv","r",encoding='utf-8')
	obj=csv.reader(file2)
	for links in obj:
		for link in links:
			print(link)
			links_set.add(link)
	file2.close()
except:
	pass

#############################################################

if write_file:
    file=open("scrape"+idx+".csv","a",encoding='utf-8')
    headers="Topicname,thread_author,views,post_author,date,posttext\n"
    file.write(headers)

    file2=open("final_links"+idx+".csv","a",encoding='utf-8')
    #file2.write("links scraped\n")



print("ENTER THE NUMBER OF LINKS U WANT TO SCRAP TOGETHER")
linknum=int(input())

base_url_list=[]
base_lower=[]
base_upper=[]

for jj in range(linknum):
    print("enter the url containing links to posts u wanna scrape")
    new_url=str(input())
    base_url_list.append(new_url)
    
    print("ENTER THE LOWER LIMIT FOR THIS BASE_URL")
    n=int(input())
    base_lower.append(n)
    
    print("ENTER THE UPPER LIMIT FOR THIS BASE_URL")
    n=int(input())
    base_upper.append(n)


#############--STARTING SCRAPING--##############

base_counter=-1

for base_url in base_url_list:
    try:
        base_counter+=1
        print("BASE_URL=",base_url)

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

        nn=min(nn,base_upper[base_counter])                        ###
        print("NUMBER OF PAGES WITH LINKS:",nn - base_lower[base_counter],"\n")

        #######################################
        zz=0
        zz=base_lower[base_counter]                                ###                                             ##
        for zz in range( base_lower[base_counter] , nn ):
            try:
                # PAGE LINK TRAVERSAL
                print("SCRAPING PAGE WITH POST LINKS : ",zz+1)

                new_url=base_url+"&st="+str(zz*40)

                # if new_url in links_set:
                #     continue
                # else:
                #     links_set.append(new_url)

                uClient=uReq(base_url+"&st="+str(zz*40))
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

                        if str(linkboxes)=="None" or len(linkboxes)==0:
                            #print("\nERROR\n")
                            continue
                        
                        for h in linkboxes:
                            linkboxdata.append(h.text.strip())

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

                            if str(linkboxes2)=="None"or len(linkboxes)==0:
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
                        # topicname=topicname.strip()
                        # topicname=topicname.replace(","," ")
                        # topicname=topicname.replace("\n"," ")

                        # thread_author=thread_author.strip()
                        # thread_author=thread_author.replace(","," ")
                        # thread_author=thread_author.replace("\n"," ")

                        # views=views.strip()
                        # views=views.replace(","," ")
                        # views=views.replace("\n"," ")
                        

                        cnt+=1
                        
                        if test and cnt>test_limit:
                                    break
                        if print_topic:        
                            print("topicname:",topicname," thread_author",thread_author," views",views,"\nlink",link,"\n")

                        # NOW THE LINK NEED TO BE SCRAPED 





                        my_url=link

                        if link in links_set:
                            print("DUPLICATE LINK")
                            continue
                            
                        if write_file:
                            print("WRITING TO LINK_F")
                            kkk=0
                            kkk=file2.write(link+"\n")
                            if kkk:
                                print("SUCCESSFULL LINK PRINTING")

                        links_set.add(link)






                        uClient=uReq(my_url)
                        page_html = uClient.read()
                        uClient.close()

                        soup = bsoup(page_html,"html.parser")

                        #posts=soup.findAll("div",{"class":"postcolor"})

                        ###############################

                        headings=soup.findAll("td",{"nowrap":"nowrap"})

                        # print(headings[len(headings)-1].text.strip())  # gives number of pages after including this page
                        # headings =  Pages: (24)  [1]  2  3  ...  Last »   ( Go to first unread post ) 
                        n=1
                        if str(headings)!="None"  and len(headings)>0:
                            s=headings[len(headings)-1].text.strip()
                            try:
                                s=s[s.find("(")+1:s.find(")")]
                                #print(s)
                                n=int(s)      # number of pages to be scraped i=1 to n-1 add  i*15 to url
                            except:
                                pass
                        print("NUMBER OF PAGES:",n,"\n")

                        #print("&st=",i*40)
                        marker="&st="+str(zz*40)
                        i=0                                                                                  ##

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

                                                if print_post:
                                                    print("\nusername:",username,"\nposttext:",posttext,"\ndate:",date,"\nquote",quote,"\n")
                                                u=username.replace(","," ")
                                                u=u.replace("\n"," ")
                                                d=date.replace(","," ")
                                                d=d.replace("\n"," ")
                                                p=posttext.replace(","," ")
                                                p=p.replace("\n"," ")
                                                post_count+=1

                                                if write_file:
                                                    file.write(topicname+","+thread_author+","+views+","+u+","+d+","+p+"\n")


                                                if clear and post_count%clear_limit==0:
                                                    os.system('cls')   # for windows
                                                    tmp=sp.call('clear',shell=True)

                                
                                print("POSTS SCRAPED:", post_count,"       thread_author="+thread_author+"       "+base_url+marker+"  "+idx )

                            except:
                                print("ERROR WITH POST PAGE")
                                #pass
                                continue

            except:
                print("ERROR WITH POST LINKS PAGE")
                continue

    except:
        print("ERROR WITH BASE URL")
        continue


if write_file:
    print("CLOSING FILE")
    file.close()
    file2.close()