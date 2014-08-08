from BeautifulSoup import BeautifulSoup as soup
from subprocess import Popen, PIPE
import subprocess
import urllib2, os, downloadchunks

def findinlist(lst, predicate):
    return (i for i, j in enumerate(lst) if predicate(j)).next()

try:
    #get current version number from website
    print "attempting to upgrade the package 'Anki'..."
    #collect data from website and process
    html = soup(urllib2.urlopen("http://ankisrs.net/"))
    alllinks = [tag.attrMap['href'] for tag in html.findAll('a', {'href': True})]
    alllinks_string = ''.join(str(x) for x in alllinks)
    #print alllinks_string
    deblocation = alllinks_string.find('.deb')
    slash_to_versionnumber_location = alllinks_string.rfind('/',0,deblocation)
    ankiwebversion = alllinks_string[slash_to_versionnumber_location+6:deblocation]
    print 'anki web version:', ankiwebversion
    
    #get version on machine
    (stdout, stderr) = Popen(["apt-show-versions","anki"], stdout=PIPE).communicate()
    machineversion = stdout
    machine_space_location = machineversion.find(' ',9)
    machineversion = machineversion[9:machine_space_location]
    machineversion = machineversion.replace(' ','-',1)
    print 'machine version:', machineversion
    
    #test if versions match
    if ankiwebversion == machineversion:
        print 'versions match!'
    else:
        print 'upgrading Anki...'
        #download file
        hreflistlocation = findinlist(alllinks, lambda x: ankiwebversion+'.deb' in x)
        deburl = alllinks[hreflistlocation]
        os.chdir('/tmp/')
        print "downloading file..."
        f = urllib2.urlopen(deburl)
        data = f.read()
        with open(ankiwebversion+".deb", "wb") as code:
            code.write(data)
        print "finished downloading. Installing anki..."
        (stdout, stderr) = Popen(["dpkg","-i","/tmp/"+ankiwebversion+".deb"], stdout=PIPE).communicate()
        print stdout
        
        print 'dpkg finished.'
    
except Exception:
    print "Unable to update Anki."
