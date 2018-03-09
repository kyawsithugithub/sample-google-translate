from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import urllib
import urllib2
from urlparse import urlparse
from StringIO import StringIO
from coolbot.models import Photo,fbUser,language

#from models import photo
from django.core.files.temp import NamedTemporaryFile
#import urllib

from io import BytesIO
#from urllib.request import urlopen

from django.core.files import File


# url, filename, model_instance assumed to be provided
#response = urlopen(url)
#io = BytesIO(response.read())
#model_instance.image_field.save(filename, File(io))

# Create your views here.

def translatenormaltext(request):
    fbID=request.GET.get('fb_id')
    firstName=request.GET.get('fb_first_name')
    lastName=request.GET.get('fb_last_name')
    gender=request.GET.get('fb_gender')
    timeZone=request.GET.get('fb_timezone')
    plainText=request.GET.get('plaintext')
    locale=request.GET.get('fb_locale')
    oringintext=request.GET.get('origintext')
    #oringintext.encode('ascii','ignore')
    
    count=checkOldUser(firstName,lastName)
    #preferLanguage=checkPreferLanguage(firstName,lastName)
    if count== 0:
        saveUser(fbID,firstName,lastName,gender,timeZone,locale,'en')
    
    preferLanguage=checkPreferLanguage(firstName,lastName)
    #preferLanguage="en"
    #oringintext=request.GET.get('plain')
    #preferLanguage='fr'
    url= 'https://www.googleapis.com/language/translate/v2?key={google-translate-api-key}&target=%s&q='%preferLanguage
    urltext=urllib.quote(plainText)      
    completeurl=url+urltext
    json_string = urllib2.urlopen(completeurl)
    json_data = json.load(json_string)
    text = '{"messages": [{"text":"',json_data["data"]["translations"][0]["translatedText"],'"}]}'
    #refurl=request.GET.get('ref')
    #print(refurl);
    #imgurl=request.GET.get('fb_profile_pic')
    #gender=request.GET.get('fb_gender')
    #boyorgirl=''
    #if(gender == 'male'):
    
        #boyorgirl='boy'
    
    #else:
        #boyorgirl='girl'
    #text = '{"messages": [{"text": "Hello ' ,myVar , ' How are you!"},{"text": "Are you a ', boyorgirl ,'?"},{"attachment": {"type": "image","payload": {"url": "',imgurl,'"}}},{"text": "Who is this stupid guy?"}]}'
    #text = '{"messages": [{"text": "' ,fbID,',',firstName,',',lastName,',',gender,',',timeZone,',',plainText,',',locale, '"}]}'
    #text='{"messages": [{"text":"Doraemon "}]}'
    return HttpResponse(text)
    
def saveUser(fbid,fname,lname,g,tzone,loc,prelang):
    tempUser=fbUser(fbID=fbid,
			firstName=fname, 
			lastName=lname,
			gender=g,
			timeZone=tzone,
			locale=loc,
			preferLanguage=prelang
		)
    tempUser.save()
 
def chooselanguage(request):
    
    firstName=request.GET.get('fb_first_name')
    lastName=request.GET.get('fb_last_name')
    languageName=request.GET.get('languageName')
    fbID=request.GET.get('fb_id')
    gender=request.GET.get('fb_gender')
    timeZone=request.GET.get('fb_timezone')
    locale=request.GET.get('fb_locale')
    text='{"messages": [{"text":"Nothing is changed."}]}'
    
    print(languageName)
    langdata=checkLanguage(languageName)
    #lcount=langdata.count()
    if langdata > 0:
        langcode=getLangCode(languageName)
        
        print(langcode)
        
        ucount=checkOldUser(firstName,lastName)
        #preferLanguage=checkPreferLanguage(firstName,lastName)
        if ucount > 0:
            print('update')
            updateUser(firstName,lastName,langcode)
            text = '{"messages": [{"text":"Language is changed."}]}'
        else:
            saveUser(fbID,firstName,lastName,gender,timeZone,locale,langcode)
            text = '{"messages": [{"text":"Language is changed."}]}'
    else:
        text='{"messages": [{"text":"Nothing is changed."}]}'
    
    #print("Hello")
    #text = '{"messages": [{"text":"Hello"}]}'
    return HttpResponse(text)
    
    

def checkLanguage(lname):
    langdata=language.objects.filter(languageName=lname).count()
    return langdata
    
def getLangCode(lname):
    langdata=language.objects.filter(languageName=lname)
    langcode=langdata[0].code
    return langcode
    
def updateUser(fname,lname,preferlanguage):
    fbUser.objects.filter(firstName=fname,lastName=lname).update(preferLanguage=preferlanguage)
    print('updated')
    
    
def checkOldUser(fname,lname):
    qryCount=fbUser.objects.filter(firstName=fname,lastName=lname).count()
    return qryCount
    
def checkPreferLanguage(fname,lname):
    objUser=fbUser.objects.filter(firstName=fname,lastName=lname)
    language=objUser[0].preferLanguage
    #language=languageQry.checkPreferLanguage[0]
    
    #print(language)
    #language='en'
    return language
    
def imagedetect(request):
    
    fbID=request.GET.get('fb_id')
    firstName=request.GET.get('fb_first_name')
    lastName=request.GET.get('fb_last_name')
    gender=request.GET.get('fb_gender')
    timeZone=request.GET.get('fb_timezone')
    plainText=request.GET.get('plaintext')
    locale=request.GET.get('fb_locale')
    
    #img_url = 'https://scontent.xx.fbcdn.net/v/t35.0-12/16930508_1359240580802932_1948411196_o.jpg?_nc_ad=z-m&oh=8aca3b623ae07646daf0b84d078f9afe&oe=58B32B4E'
    img_url = request.GET.get('ref')
    photo = Photo()    # set any other fields, but don't commit to DB (ie. don't save())
    name = urlparse(img_url).path.split('/')[-1]
    content = urllib.urlretrieve(img_url)
    photo.image.save(name, File(open(content[0])), save=True)
    
    
    ocrimgurl='https://api.ocr.space/parse/imageurl?apikey={ocr-space-api-key}&language=chs&isOverlayRequired=true&url='#+'name'
    imgurl='https://coolbot-final-kyawsithugithub.c9users.io/path/'+name #local host url
    #print(imgurl)
    urltext=urllib.quote(imgurl)
    completeurl=ocrimgurl+urltext
    #print(completeurl)
    json_string = urllib2.urlopen(completeurl)
    json_data = json.load(json_string)
    detected=json_data['ParsedResults'][0]['ParsedText']
    detected.encode('ascii','ignore')
    detected=detected[:-2]
    if detected.count > 0:
    
    #/////////////////////////////////
    
        count=checkOldUser(firstName,lastName)
        if count== 0:
            saveUser(fbID,firstName,lastName,gender,timeZone,locale,'en')
    
        preferLanguage=checkPreferLanguage(firstName,lastName)
    
        url= 'https://www.googleapis.com/language/translate/v2?key={google-translate-api-key}&target=%s&q='%preferLanguage
        urltext=urllib.quote(detected)      
        completeurl=url+urltext
        json_string = urllib2.urlopen(completeurl)
        json_data = json.load(json_string)
        text = '{"messages": [{"text":"',json_data["data"]["translations"][0]["translatedText"],'"}]}'
    
        #return HttpResponse(text)
    
    #////////////////////////////////
    
    else:
        text = '{"messages": [{"text":"Text cannot detect"}]}'
        #print(text)
    return HttpResponse(text)
    
    
    
def getimage(request,para):
    
    
    
    return HttpResponse(para)
    
