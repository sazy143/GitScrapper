#libraries for getting and parsing html
import bs4
from bs4 import BeautifulSoup
from requests import get
import mysql.connector

#get the information from site
url = "https://github.com/sazy143?tab=repositories"
response = get(url)

#create soup parser for our html
soup = BeautifulSoup(response.text, 'html.parser')

#create empty arrays to hold our data
RepoName = []
RepoDesc = []
RepoURL = []

#select the div with the repo info
allrepos = soup.find_all('div', attrs = {'id':'user-repositories-list'})

#get each li in its own object
for ob in allrepos:
    lis = ob.find_all('li')


#loop through each li 
for li in lis:
    #convert to string so we can create BS parser
    listr = str(li)
    soup2 = BeautifulSoup(listr, 'html.parser')

    #find the proper a tag
    a = soup2.find('a', itemprop="name codeRepository")

    #make sure we found the item
    if(isinstance(a,bs4.element.Tag)):
        #apend items to respected list
        RepoName.append(a.get_text().strip())
        RepoURL.append('https://github.com'+a.get('href'))
    #not found situation
    else:
        RepoName.append('repo name not found')
        RepoURL.append('repo url not found')

    #try to find description
    p = soup2.find('p', itemprop="description")

    #desc found
    if(isinstance(p, bs4.element.Tag)):
        RepoDesc.append(p.text.strip())
    #desc not found
    else:
        RepoDesc.append('repo description not found')

#create a list of lists with all our info to use as the params in executemany
RepoList = []
for i in range(len(RepoName)):
    RepoList.append([RepoName[i],RepoDesc[i],RepoURL[i]])
print(RepoList)


try:
    #connect to database
    connection = mysql.connector.connect(
        host = 'localhost',
        database = 'test',
        user = 'root',
        password = '')
    print('connected to server')
    #run sql to clear our table of previous data (start fresh)
    sql = 'DELETE FROM repositories'
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()

    #insert all the records we found from the webcrawler
    insertsql = 'INSERT INTO repositories VALUES( %s, %s, %s)'
    cursor1 = connection.cursor()
    cursor1.executemany(insertsql,RepoList)
    cursor1.close()

    #commit our changes since this is off by default
    connection.commit()
    

except mysql.connector.Error as error:
    print('ran into error',error)

finally:
    #close our connection
    connection.close()



