NAME = "RTBF"
ART = "art-default.jpg"
ICON = "icon-default.jpg"
PREFIX = '/video/rtbf'

SHOWS_URL = "https://www.rtbf.be/auvio/emissions"

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
	#HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'

####################################################################################################
@handler(PREFIX, NAME, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(ShowsMenu, title="Emissions"), title="Emissions"))
	#oc.add(InputDirectoryObject(key=Callback(SearchMenu, title="Search PBS"), title="Search PBS"))
	oc.add(PrefsObject(title = L('Preferences')))

	return oc

####################################################################################################
@route(PREFIX + '/showmenu')
def ShowsMenu(title):

    oc = ObjectContainer(title2=title)
    page = HTML.ElementFromURL(SHOWS_URL)

		shows_elements = page.xpath("//article[@class='rtbf-media-item']")

		for show_elem in shows_elements:
  		show_title = show_elem.xpath("//a[@class='www-faux-link']//@title")[0]
			thumb = show_elem.xpath('.//img/@data-srcset')[0].split(',')[0].split(' ')[0]

			oc.add(DirectoryObject(key=Callback(GetShowVideos, id=show_id), 
				title = show_title,
				thumb = Resource.ContentsOfURLWithFallback(url=thumb)
			))


    return oc
