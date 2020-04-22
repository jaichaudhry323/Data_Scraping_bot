# Data_Scraping_bot
Data_Scraping_bot for this site -->  https://forum.ge/?act=idx

On windows powershell prompt go to folder directory in which scrapper file is present 

Write on powershell or on terminal of ubuntu
python scrapper.py  (for windows)  OR ELSE    python3 scrapper.py    (for ubuntu)

then go to this site https://forum.ge/?act=idx

Copy the link of any topic U want to scrape from then paste it in the powershell when the program asks for link
E.g U can choose Politics , Science and Education , Melomania , cinema , Photography   topic's link 


E.g TRY RUN --> 

PS D:\Jai\To_be_uploaded_to_github\Scraping> D:\Jai\To_be_uploaded_to_github^C
PS D:\Jai\To_be_uploaded_to_github\Scraping> python scraper.py
1->write to file , 0-> dont write to file
1 
ENTER TABLE NUMBER 0 or 1 or 2
1 
ENTER FILE NUMBER
2 
SURE U WANNA CREATE THIS FILE ?? 0 or 1
1 
ENTER THE NUMBER OF LINKS U WANT TO SCRAP TOGETHER
2 
enter the url containing links to posts u wanna scrape
https://forum.ge/?showforum=29
ENTER THE LOWER LIMIT FOR THIS BASE_URL
0
ENTER THE UPPER LIMIT FOR THIS BASE_URL
1000
enter the url containing links to posts u wanna scrape
https://forum.ge/?showforum=20
ENTER THE LOWER LIMIT FOR THIS BASE_URL
0
ENTER THE UPPER LIMIT FOR THIS BASE_URL
1000
BASE_URL= https://forum.ge/?showforum=29
NUMBER OF PAGES WITH LINKS: 52

SCRAPING PAGE WITH POST LINKS :  1
TOTAL ROWS= 43
D
topicname: საგანგებო მდგომარეობა ქვეყანაში  thread_author IOSKAMAN  views 5307
link https://forum.ge/?s=a352a72837f0b6518e3a61c868793d20&f=29&showtopic=35145694

WRITING TO LINK_F
SUCCESSFULL LINK PRINTING
NUMBER OF PAGES: 3

SCRAPING PAGE :  1

username: IOSKAMAN
posttext: 2020 წლი
quote

.......( SCRAPED DATA ).....

POSTS SCRAPED: 16        thread_author=IOSKAMAN       https://forum.ge/?showforum=29&st=0  _1_2
SCRAPING PAGE :  2

.......( SCRAPED DATA ).....

And so on
