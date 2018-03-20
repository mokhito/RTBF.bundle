NAME = "RTBF"
ART = "art-default.jpg"
ICON = "icon-default.jpg"
PREFIX = '/video/rtbf'

PARTNER_KEY = "82ed2c5b7df0a9334dfbda21eccd8427"

SHOWS_URL = "https://www.rtbf.be/auvio/emissions"
MEDIA_LIST_JSON = "https://www.rtbf.be/api/partner/generic/media/objectlist?v=8&program_id=%s&target_site=mediaz&offset=0&limit=10&partner_key=%s"

SHOW_IDS = {
	"laune": "",
	"ladeux": "",
	"latrois": "",
	"lapremiere": "",
	"vivacite": ""
}

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'

####################################################################################################
@handler(PREFIX, NAME, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(ShowsMenu, title="La Une", key="laune"), title="La Une"))
	oc.add(DirectoryObject(key=Callback(ShowsMenu, title="La Deux", key="ladeux"), title="La Deux"))
	oc.add(DirectoryObject(key=Callback(ShowsMenu, title="La Trois", key="latrois"), title="La Trois"))
	oc.add(DirectoryObject(key=Callback(ShowsMenu, title="La Première", key="lapremiere"), title="La Première"))
	oc.add(DirectoryObject(key=Callback(ShowsMenu, title="Vivacité", key="vivacite"), title="Vivacité"))
	oc.add(DirectoryObject(key=Callback(ShowsMenu, title="Toutes les émissions RTBF", key="all"), title="Toutes les émissions RTBF"))
	#oc.add(InputDirectoryObject(key=Callback(SearchMenu, title="Search PBS"), title="Search PBS"))
	oc.add(PrefsObject(title = L('Preferences')))

	return oc

####################################################################################################
@route(PREFIX + '/showmenu')
def ShowsMenu(title, key):

	oc = ObjectContainer(title2=title)
	page = HTML.ElementFromURL(SHOWS_URL)

	shows_elements = page.xpath("//article[contains(@class, 'rtbf-media-item')]")

	for show_elem in shows_elements:
		show_id = show_elem.xpath("@data-id")
		show_title = show_elem.xpath(".//a[@class='www-faux-link']/@title")[0]
		thumb = show_elem.xpath('.//img/@data-srcset')[0].split(',')[0].split(' ')[0]

		oc.add(DirectoryObject(key=Callback(GetShowVideos, title=show_title, show_id=show_id), 
			title = show_title,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb)
		))


	return oc

####################################################################################################
@route(PREFIX + '/getshowvideos')
def GetShowVideos(title, show_id):

	oc = ObjectContainer(title2=title.encode("utf-8"))
	
	json_url = MEDIA_LIST_JSON % (show_id, PARTNER_KEY)
	videos = JSON.ObjectFromURL(json_url, headers={"X-Requested-With": "XMLHttpRequest"})

	for video in videos:
		stream_url = video["url_embed"] if video["is_external"] == "1" else video["url_streaming"]["url_high"]
		video_title = video["title"].encode("utf-8")
		#video_show = video["program"]["label"].encode("utf-8")
		video_desc = video["description"].encode("utf-8")
		#duration = video["duration"]
		thumb = Resource.ContentsOfURLWithFallback(url=video["images"]["illustration"]["16x9"]["770x433"], fallback="icon-default.jpg")
		
		oc.add(CreateVideoObject(show_id, stream_url, video_title, video_desc, thumb))

	return oc

####################################################################################################
@route(PREFIX + '/video')
def CreateVideoObject(show_id, stream_url, title, summary, thumb, include_container=False, **kwargs):
  video_obj = VideoClipObject(
		key=Callback(CreateVideoObject, show_id=show_id, stream_url=stream_url, 
									title=title, summary=summary, thumb=thumb, 
									include_container=True),
		rating_key=show_id,
		title=title,
		summary=summary,
		thumb=thumb,
		items=[
			MediaObject(
				parts=[
					PartObject(key=HTTPLiveStreamURL(stream_url))
				],
				video_resolution = '720',
				audio_channels = 1,
				optimized_for_streaming = True
			)
		]
  )

  if include_container:
    return ObjectContainer(objects=[video_obj])
  else:
		return video_obj

