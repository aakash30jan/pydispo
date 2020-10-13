#!/usr/bin/env python3

"""
pydispo - Disposable Mailbox Powered by Pure-Python
By Aakash Patil

url="https://github.com/aakash30jan/pydispo"
version="20.10b1"
license="GNU General Public License, version 3"
"""

from __future__ import print_function
import sys
import argparse
import os
import random
import string
import requests
import webbrowser


#config
cache_tag = 'TEMP' #Options: CWD, <UD>

#os check
if os.name == 'nt':
    temp_dir = os.path.expanduser('~')+r'\\AppData\\Local\\Temp\\'
else:
    temp_dir = "/tmp/" 

#cache location
if cache_tag == 'TEMP':
    if not os.path.exists(temp_dir):
        temp_dir = ".tmp"
    pydispo_workdir = temp_dir+'pydispo'
elif cache_tag == 'CWD':
    pydispo_workdir = os.getcwd()
else:
    #Get from args pydispo_workdir = 
    pydispo_workdir = os.getcwd()
    
pydispo_emailaddr_cache = pydispo_workdir+"/dispomail.addr"
pydispo_emailhtml_cache = pydispo_workdir+"/dispomail.html"

if not pydispo_workdir == os.getcwd():
    if not os.path.exists(pydispo_workdir):
        os.mkdir(pydispo_workdir)
 
def generate_email_address(size=10,storeInFile='email_address',mode='w'):
    tld_list=['com', 'net', 'org']
    chars=string.ascii_lowercase + string.digits
    user = ''.join(random.SystemRandom().choice(chars) for _ in range(size))
    email_addr = user+'@1secmail.'+ random.choice(tld_list)
    fop = open(storeInFile,mode)
    if mode == 'a':
      fop.write(email_addr+'\n')
    else:  
      fop.write(email_addr)
    fop.close()
    print("Generated: ", email_addr)
    return email_addr; 
    #FUTURE: HUMAN_NOM_PRENOM@platforme.CHOICE 
    
def get_email_address(checkFile=pydispo_emailaddr_cache, getNew=False):
    if getNew:
        email_addr = generate_email_address(size=10,storeInFile=checkFile)
        return email_addr ; 
    if os.path.exists(checkFile):
        fop = open(checkFile).readlines()
        #print("Found email address: ", fop)
        email_addr = fop[0]
    else:
        print("No email address found, generating new")
        email_addr = generate_email_address(size=10,storeInFile=checkFile)
    return email_addr ; 
    #FUTURE: encrypted history obj

def check_mailbox(email_addr,showInbox=True,showRecent=True):
    login_id = email_addr[:email_addr.find('@')]
    login_domain = email_addr[email_addr.find('@')+1:]
    http_get_url =   "https://www.1secmail.com/api/v1/?action=getMessages&login="+login_id+"&domain="+login_domain
    response = requests.get(http_get_url)
    
    if not response.status_code == 200:
        print("Invalid server response code ", response.status_code)
        return ;

    response = response.json()
    num_mails = len(response)
    if num_mails == 0:
        print("Mailbox: ", email_addr, " Mails in Inbox:",num_mails )
        print("Empty Inbox")
        return ;

    inboxmail_id_list = []
    print("#"*25)
    print("Mailbox: ", email_addr, " Mails in Inbox:",num_mails )
    for nm in range(num_mails):
        if showInbox:
            if nm == 0:
                print('Message ID' ,'\t', 'Sender' ,'\t \t', 'Subject', '\t' , 'Date')
            print(response[nm]['id'] ,'\t', response[nm]['from'] ,'\t', response[nm]['subject'].encode("utf-8"), '\t' , response[nm]['date'] )
        inboxmail_id_list.append(response[nm]['id'])
    
    if showRecent:
        print("Showing the recent email received on: "+response[0]['date'])
        check_single_email(email_addr,inboxmail_id = inboxmail_id_list[0])
    print("#"*25)
    return;     
    #FUTURE: A proper protonmail-style layout

def check_single_email(email_addr,inboxmail_id = 0, bodyasHTML = False, getAttached=False, saveHTMLFile="tmpmail.html",printInTerminal=True):
    login_id = email_addr[:email_addr.find('@')]
    login_domain = email_addr[email_addr.find('@')+1:]
    http_get_url_single =   "https://www.1secmail.com/api/v1/?action=readMessage&login="+login_id+"&domain="+login_domain+"&id="+str(inboxmail_id)
    response = requests.get(http_get_url_single)
    
    if not response.status_code == 200:
        print("Invalid server response code ", response.status_code)
        return ;
    
    if response.content.decode("utf-8") == 'Message not found':
        print("No message found with", inboxmail_id)
        return ;
    
    response = response.json()
    if len(response['attachments']) == 0: 
        str_attached = 'Not Found'
        getAttached = False
        num_files = 0
    else:
        json_att = response['attachments']
        num_files = len(json_att)
        str_attached = []
        attached_files = []
        for nf in range(num_files):
            str_attached.append(json_att[nf]['filename']+'   ('+json_att[nf]['contentType']+')   '+str(round(json_att[nf]['size']/1E6,3))+' MB approx')
            attached_files.append(json_att[nf]['filename'])
            
    if bodyasHTML:
        email_body = makeHTMLPage(email_addr, response , str_attached) #response['htmlBody']
        fop = open(saveHTMLFile,'w')
        fop.write(email_body.encode("utf-8"))
        fop.close()
        email_body = "Saved as HTML in "+saveHTMLFile
    else:
        email_body = response['textBody']

    if printInTerminal:        
          print("ID: ", response['id'])
          print("To: ", email_addr)
          print("From: ", response['from'])
          print("Date: ", response['date'])
          print("Subject: ", response['subject'].encode("utf-8"))
          print("Attachments: ", str_attached)
          try:
            print("--------------------\n",email_body )
          except:  
            print("--------------------\n",email_body.encode("utf-8") )
          print("--------------------")

    if getAttached:
        print("Getting all attached files . . ")
        for filename in attached_files:
            getAttachedFile(http_get_url_single, filename,savedir='./')
    return ;
    #FUTURE: All to HTML, not just body. Link Attachments to HTML. Store attachments in workdir
    
def getAttachedFile(http_get_url_single, filename,savedir='./'):
    http_get_url_attached = http_get_url_single.replace("action=readMessage","action=download")+"&file="+filename
    print("Getting attached file:", filename)
    response = requests.get(http_get_url_attached)
    
    if not response.status_code == 200:
        print("Invalid server response code ", response.status_code)
        return ;
    
    open(savedir+filename, 'wb').write(response.content)
    print("Downloaded to: ",savedir+filename)
    return;
    #FUTURE: file size verify downloaded vs server

def makeHTMLPage(email_addr, response , str_attached):
    if len(response['attachments']) > 0: 
        ulList = ["<ul>"]
        for fdsp in str_attached:
            ulList.append("<li> "+fdsp+" </li>")
        ulList.append("</ul>")
    else:
        ulList = []

    full_htmail = "<html><body><h3> "+response['subject'] +" </h3><hr> Message-id: "+ str(response['id']) +"<br> From: <b> "+response['from']+" </b>  <br> To: "+ email_addr +"  <br> Date & Time: "+response['date']+" <br> <hr> <hr> "+ ''.join(response['htmlBody'])+" <hr>  "+str(len(response['attachments']))+" file(s) attached. "+ ''.join(ulList) +"<hr> </body> </html> "
    return full_htmail ; 

def use_browser(browser_name='lynx',url='https://www.google.fr/'):
    try:
        controller = webbrowser.get(browser_name)
    except:
        print("Unable to locate web browser ", browser_name)
        return ;
    if not os.path.exists(url):
        print("Unable to open email as HTML file ", url)
        return;
    controller.open_new(url) #_new_tab open(url, new=0, autoraise=True)
    return;
    #Future: Find verify, subscribe etc to click and visit. Set cookie stuff True, clean caches before exit.

def flush_all(pydispo_workdir,attached=False):
    print("Not implemented")
    return ; 

def enc_dec(pydispo_workdir):
    print("Not implemented")
    return ; 

def backup_previous(pydispo_workdir,attached=False):
    print("Not implemented")
    return ; 

def main():
    parser = argparse.ArgumentParser(description='pydispo - Disposable Mailbox Powered by Pure-Python',epilog='Cheers :)') 
    parser.add_argument("id", type=int, default=0, nargs='?', help="Check an email with given message ID" )
    parser.add_argument("-a", "--attached", action='store_true', default=False, required=False, help="Download all attached files in the email" )
    parser.add_argument("-r", "--recent", action='store_true', default=False, required=False, help="Check the most recent email" )
    parser.add_argument("-g", "--generate", action='store_true', default=False, required=False, help="Generate a new email address" )
    parser.add_argument("-s", "--save", action='store_true', default=False, required=False, help="Save email in an HTML file" )
    parser.add_argument("-b", "--browser", type=str, default='TextOnly', required=False, help="Browser to check the email in HTML" )
    parser.add_argument("-e", "--email", type=str, default='NONE@1secmail.com', required=False, help="Check mailbox of a particular email" )
    args = parser.parse_args()
    #Take care of parsed arguments
    particularID = args.id
    getAttached = args.attached
    showRecent = args.recent
    getNew = args.generate
    bodyasHTML = args.save
    browser_name = args.browser
    email_addr = args.email

    if email_addr == 'NONE@1secmail.com':
        email_addr = get_email_address(pydispo_emailaddr_cache,getNew)
        if getNew:
            sys.exit()

    if particularID == 0:
        #Show recent and exit
        if showRecent:
            check_mailbox(email_addr,showInbox=False,showRecent=True)
        #Show mailbox and exit
        else:
            check_mailbox(email_addr,showInbox=True,showRecent=False)
        sys.exit()
    else:
        showInbox = False

    if not browser_name == 'TextOnly':
        #check particular email in browser_name 
        check_single_email(email_addr,inboxmail_id = particularID, bodyasHTML = True, getAttached=getAttached, saveHTMLFile = pydispo_emailhtml_cache,printInTerminal=False)
        use_browser(browser_name=browser_name,url=pydispo_emailhtml_cache)

    else:
        #check particular email #save as HTML #get attachments
        check_single_email(email_addr, particularID, bodyasHTML, getAttached, pydispo_emailhtml_cache)

    return ; 


if __name__ == "__main__":
    main()


