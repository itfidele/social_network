from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    data = list()
    return HttpResponse('<h1>Salam Bro</h1>')


def yego(request):
    return HttpResponse('<h2>Yego Moto</h2>')


headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"


@csrf_exempt
def webhook(request):
    results = json.loads(request.body)
    artistname = results['queryResult']['parameters']['music-artist']
    musicname = results['queryResult']['parameters']['music-name']
#timesLocation = results['queryResult']['parameters']['wheretime']
    # if timesLocation is not None:
    #data = timeScrap(timesLocation)
    if artistname is not None and musicname is not None:
        data = link_lyrics(artistname, musicname)
    result = {
        'fulfillmentText': data,
    }

    return JsonResponse(result, safe=False)


def timeScrap(timess):
    dat = urllib.parse.quote(timess+" time")
    url = "https://www.google.com/search?q="+dat
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    bs = BeautifulSoup(respData, 'html.parser')
    timess2 = bs.find(class_='gsrt vk_bk dDoNo').get_text()
    return str(timess2)


def lyrics_text(url):
    reqo = urllib.request.Request(url, headers=headers)
    se = urllib.request.urlopen(reqo).read()
    ddd = BeautifulSoup(se, 'html.parser')
    try:
        m = ddd.find(class_='lyrics__content__warning').get_text()
    except:
        m = ddd.find(class_='lyrics__content__ok').get_text()
    return m


def link_lyrics(artistname, musicname):
    dat = urllib.parse.quote(
        "site:musixmatch.com "+musicname+" by"+" "+artistname+" lyrics")
    url = "https://google.com/search?q="+dat
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers=headers)
    respData = urllib.request.urlopen(req).read()
    bs = BeautifulSoup(respData, 'html.parser')
    ff = bs.find_all(class_='g')
    m = ff[0].find('a', href=True)['href']
    return str(m)


def lyrics(request):
    song = request.GET.get('link')
    result = {
        "lyrics": lyrics_text(song)
    }
    return JsonResponse(result, safe=False)


def googleSearch(request):
    if request.POST.get('search') is not None:
        value = request.POST.get('search')
        try:
            dat = urllib.parse.quote(value)
            url = "https://www.google.com/search?q="+dat
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = resp.read()
            bs = BeautifulSoup(respData, 'html.parser')
            for datame in bs.find_all(class_='g'):
                title = datame.find(class_='LC20lb').get_text()
                content = datame.find(class_='st').get_text()
                link = datame.find('a')['href']
                data.append(
                    {
                        "title": title,
                        "content": content,
                        "link": link,
                    }
                )
            return JsonResponse(data, safe=False)
        except Exception as e:
            print("")