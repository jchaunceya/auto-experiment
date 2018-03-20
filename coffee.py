import time,random,threading,re,itertools,pandas,requests,copy,bs4, concurrent.futures,time
from selenium import webdriver
import random
import numpy as np
logindata={'targetpage':'', 'email':'jchaunceya', 'word':'peenfeen', "Sign In":"Sign In"}
loginposturl = 'http://island.maths.uq.edu.au/login.php'
username = "JCHAUNCEYA"
password = "peenfeen"
loginurl = "http://island.maths.uq.edu.au/access.php?/index.php"
baseurl = 'http://island.maths.uq.edu.au{}'
profileurl = 'http://island.maths.uq.edu.au/show.php?id={}'
task1 = 'coffee'
task2 = 'water250'
task3 = ''
response_task = 'memorygame'
ids = []
task1_counter = 0
task2_counter = 0
task1_limit = 20
task2_limit = 20
counter = 0

regroup = pandas.DataFrame()


def login_driver(driver):
    driver.get(loginurl)
    driver.find_element_by_xpath('//input[@name="email"]').send_keys(username)
    driver.find_element_by_xpath('//input[@name="word"]').send_keys(password)
    driver.find_element_by_xpath('//input[@name="Sign In"]').click()
    return driver
def run_group(df):
    driver = webdriver.Chrome()
    driver = login_driver(driver)
    [measure_start(id, driver) for id in df.id]
    s = time.time()
    tasks = list(df.task)
    time.sleep(25)
    starts = [{'start':measure_heartbeat(id), 'id':id} for id in df.id]
    starts = pandas.DataFrame(starts)
    df = df.merge(starts, on='id' )
    [run_task(task, id, driver) for task,id in zip(tasks,df.id)]
#    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
#        executor.map(run_task, tasks, list(df.id))
    for i in range(0,16):
        print("minute {}[{}]".format(i,threading.currentThread()))
        time.sleep(60)


    [measure_end(id, driver) for id in df.id]
    time.sleep(25)
    ends = [{'end':measure_heartbeat(id), 'id':id} for id in df.id]
    ends = pandas.DataFrame(ends)
    ends = [end for end in ends if end]
    ends = pandas.DataFrame(ends)
    df = df.merge(ends, on='id' )
    global regroup
    regroup = regroup.append(df)
    print(df.head())


def do_everything():
    global regroup
    df = pandas.read_csv("final-consent.csv")
    # get_consent



    temp =list(df.groupby('newage'))
    
    old = temp[1][1]
    
    young = temp[0][1]
    temp = list(old.groupby('gender'))
    old_women = temp[0][1]
    old_men = temp[1][1]
    temp = list(young.groupby('gender'))
    young_women = temp[0][1]
    young_men = temp[1][1]

    old_men = old_men.sample(48)
    old_women = old_women.sample(48)
    young_men = young_men.sample(48)
    young_women = young_women.sample(48)
    old_men_1 = old_men.iloc[0:16]

    # input task names
    # FILL IN TASK

    cat = 'petcat'
    dog = 'petdog'
    control = 'mentalhard'
    
    old_men_2 = old_men.iloc[16:33]
    old_men_3 = old_men.iloc[33:49]

    old_men_1['task'] = cat
    old_men_2['task'] = dog
    old_men_3['task'] = control
    old_women_1 = old_women.iloc[0:18]
    old_women_2 = old_women.iloc[16:33]
    old_women_3 = old_women.iloc[33:49]
    old_women_1['task'] = cat
    old_women_2['task'] = dog
    old_women_3['task'] = control
    young_women_1 = young_women.iloc[0:18]
    young_women_2 = young_women.iloc[16:33]
    young_women_3 = young_women.iloc[33:49]
    young_women_1['task'] = cat
    young_women_2['task'] = dog
    young_women_3['task'] = control
    young_men_1 = young_men.iloc[0:18]
    young_men_2 = young_men.iloc[16:33]
    young_men_3 = young_men.iloc[33:49]
    young_men_1['task'] = cat
    young_men_2['task'] = dog
    young_men_3['task'] = control
    old_men = pandas.DataFrame()
    old_men = old_men.append(old_men_1)
    old_men = old_men.append(old_men_2)
    old_men = old_men.append(old_men_3)
    old_women = pandas.DataFrame()
    old_women = old_women.append(old_women_1)
    old_women = old_women.append(old_women_2)
    old_women = old_women.append(old_women_3)
    young_men = pandas.DataFrame()
    young_men = young_men.append(young_men_1)
    young_men = young_men.append(young_men_2)
    young_men = young_men.append(young_men_3)
    young_women = pandas.DataFrame()
    young_women = young_women.append(young_women_1)
    young_women = young_women.append(young_women_2)
    young_women = young_women.append(young_women_3)
    all = [old_men, old_women, young_men, young_women]
    ts = []
    for daf in all:
        t = threading.Thread(target=run_group, args=(daf,))
        t.start()
        ts.append(t)

    for t in ts:
        t.join()



    regroup.to_csv("new-final.csv")
    # measure heartbeat
    # run task
    # wait 15 min
    # measure heartbeat
                        

# TODO: add male variable to dataframe

def measure_start(id, driver):
    try:
        get_heartbeat(id, driver)
    except:
        pass
    
    

def measure_end(id, driver):
    try:
        get_heartbeat(id, driver)
    except:
        pass


def get_heartbeat(id, driver):

    
    print('getting {} heartbeat...'.format(id))
    driver.get(profileurl.format(id))
    driver.implicitly_wait(5)
    driver.find_element_by_css_selector('#setTask a').click()
    driver.implicitly_wait(5)
    driver.find_element_by_link_text('Pulse Meter').click()
    time.sleep(5)


    

def measure_heartbeat(id):
    try:
        c=copy.deepcopy(logindata)
        c['targetpage'] = '/results.php?id={}'.format(id)
        r = requests.post(loginposturl, c)
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        data = soup.find('div', class_='resultsdata')
        if hasattr(data, 'text'):
            data = data.text
            v = re.findall("([\d]+)",data)[0]
            print('{}[{}]: {} bpm'.format(id, threading.currentThread(), v))
            return int(v)
        print('{}[{}] failed'.format(id, threading.currentThread()))
        return np.nan
    except:
        return np.nan

def run_task(task, id, driver):
    do_task(task, id, driver)

    
def get_consent2(id):
    global logindata
    global loginposturl
    global counter
    c = logindata
    c['targetpage'] = '/consent.php?id={}'.format(id)
    print(c)
    r = requests.post(loginposturl, c)
    print('here')
    if "accept" in r.text or "consent" in r.text or r.text == '':

        c['targetpage'] = '/contacts.php?add={}'.format(id)
        print("got {} consent:\t[{}]".format(id, counter))
        consent = 1
        counter += 1
        r = requests.post(loginposturl, c)        
        print('getit')
    else:
        print("didn't get consent: {}".format(id))
        consent = 0

    c['targetpage'] = '/show.php?id={}'.format(id)
    r = requests.post(loginposturl, c)

    # determine sex

    if " his " in r.text:
        male = 1
    else:
        male = 0
    return { 'consent':consent, 'id':id}

def get_consent(person):
    global logindata
    global counter
    c = logindata
    c['targetpage'] = '/consent.php?id={}'.format(person['id'])
    r = requests.post(loginposturl, c)
    if "accept" in r.text or "consent" in r.text:
        c['targetpage'] = '/contacts.php?add={}'.format(person['id'])
        print("got {} consent:\t[{}]".format(person['id'], counter))
        person['consent'] = 1
        counter += 1
        r = requests.post(loginposturl, c)        
    else:
        print("didn't get consent: {}".format(person['id']))
        person['consent'] = 0

    c['targetpage'] = '/show.php?id={}'.format(id)
    r = requests.post(loginposturl, c)

    # determine sex

    if " his " in r.text:
        person['male'] = 1
    else:
        person['male'] = 0
    return person

def do_task(task, id, driver):
    

    driver.get(profileurl.format(id))
    driver.implicitly_wait(4)
    driver.find_element_by_css_selector('#setTask a').click()
    driver.implicitly_wait(5)

    if task == 'petdog':
        driver.find_element_by_link_text('Pet Dog').click()
    elif task == 'petcat':
        driver.find_element_by_link_text('Pet Cat').click()
    else:
        driver.find_element_by_link_text('Difficult Mental Arithmetic').click()


    driver.implicitly_wait(3)

    return 

############################################################################
# def measure_response(response, id):                                      #
#     pass                                                                 #
#                                                                          #
#     driver.get(baseurl.format('results.php?id={}'.format(id)))           #
#     time.sleep(5)                                                        #
#     result = driver.find_element_by_css_selector('div.resultsdata').text #
#     result = re.sub("( seconds)", "", result)                            #
#     with open('results.txt', 'a') as file:                               #
#         file.write(task + ',' + result + ',' + id + '\n')                #
#         print(task + ',' + result + ',' + id + '\n')                     #
#         return result                                                    #
############################################################################
    
#################################################################################################################################
# class IslandThread(threading.Thread):                                                                                         #
#     def __init__(self, queue, people):                                                                                        #
#         threading.Thread.__init__(self)                                                                                       #
#                                                                                                                               #
#                                                                                                                               #
#         self.queue = queue                                                                                                    #
#         self.people = people                                                                                                  #
#     def run(self):                                                                                                            #
#                                                                                                                               #
# #        house_links = []                                                                                                     #
#         while True:                                                                                                           #
#             if self.queue.empty():                                                                                            #
#                 break                                                                                                         #
#                                                                                                                               #
#             url = self.queue.get()                                                                                            #
#             print("[{}]\turl:\t{}".format(self.queue.qsize(), url))                                                           #
#             links = scrape_people_links(url)                                                                                  #
#                                                                                                                               #
# #            links = [link.get_attribute('href') for link in self.driver.find_elements_by_css_selector("div.hamletlink > a")] #
#             self.people.extend(links)                                                                                         #
# #            [house_links.extend(extract_hamlet(self.driver, link)) for link in links]                                        #
#             self.queue.task_done()                                                                                            #
#             if len(people) % 25 == 0:                                                                                         #
#                 pandas.DataFrame(people).to_csv("people_links.csv")                                                           #
#   #      df = pandas.DataFrame(house_links).to_csv("island_house_links.txt")                                                  #
#################################################################################################################################



def extract_hamlet(driver,link):
    print('extracting hamlet {}'.format(link))
    driver.get(link)
    time.sleep(5)
    ls = [{'link': link.get_attribute('href')} for link in driver.find_elements_by_css_selector('div.hamletnote > a')]
    return ls
        
def extract_house_links(driver,link):
    print(link)

    driver.get(link)
    driver.implicitly_wait(2)
    ppl = []
    links = []
    try:
        things = driver.find_elements_by_css_selector('div.contactbig')
        print(things)
        for person in things:
            a = person.find_element_by_css_selector('div.age').text.split(" ")[0]
            if a >= 25 or a <= 50:
                link = driver.find_element_by_tag_name('a').getAttribute('href').split("?id=")[1]
                links.append(link)
    except Exception as e:
        print(e)
        pass


    [get_consent(driver, link) for link in links]

def intermediate(id):
    try: 
        a = get_consent(id)
        return a
    except:
        return []

def scrape_people_links(link):

    logindatacopy = copy.deepcopy(logindata)
    logindatacopy['targetpage'] = link.split(".au")[1]
    global counter
    print("{}\t{}".format(counter,logindatacopy['targetpage']))
    counter += 1
    r = requests.post(loginposturl, data=logindatacopy)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    things = soup.find_all("div", class_="contactbig")
    links = [i.a['href'] for i in things]
    names = [i.find("div",class_="resident").text for i in things]
    ages = [i.find("div",class_="age").text for i in things]
    people = [{'link':link, 'name':name, 'age': age} for link,name,age in zip(links, names,ages)]


    return people

def groups(row):
     m=row['months'] 
     if m >= (22*12) and m <= (31*12):
         row['group'] = 1
     elif m > (31*12) and m <= (41 * 12):
         row['group'] = 2
     elif m > (41 * 12) and m <= (51 *12):
         row['group'] = 3
     return row

if __name__ == "__main__":
    do_everything()
