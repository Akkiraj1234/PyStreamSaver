import requests
import re
import json

class YouTubeLinkError(Exception):
    """Error raised for invalid YouTube links."""
    def __init__(self, message='youtube link is not valid plese check again or else if link is currect contact akki instagram @akki_raj_._ or @its_just_me_akki'):
        self.message = message
        super().__init__(self.message)

class YouTube:
    def __init__(self,ytInitialPlayerResponse:json):
        '''takes ytInitialPlayerResponse json data as argumnt'''
        self.json_data=ytInitialPlayerResponse
        
    def streaming_data(self)->json:
        '''return streing data of youtube video'''
        return self.json_data.get("streamingData",None)
    
    def title(self)->str:
        '''return title of youtube video'''
        return self.json_data['videoDetails']['title']

    def artist_name(self)->str:
        '''return artist name of youtube video or chaneal name'''
        return self.json_data['videoDetails']['author']
    
    def lenth_sec(self)->int:
        '''lenth of video in sec'''
        return int(self.json_data['videoDetails']['lengthSeconds'])
    
    def lenth_milesec(self)->int:
        '''lenth of video in sec'''
        return int(self.json_data['videoDetails']['lengthSeconds'])*1000
    
    def video_id(self)->str:
        '''retrun video id of youtube video given'''
        return self.json_data['videoDetails']['videoId']
    
    def view_count(self)->int:
        '''return views of the video'''
        return int(self.json_data['videoDetails']['viewCount'])
    
    def artist_chanel_link(self)->str:
        '''retrun the link of youtube video cheanel link'''
        return self.json_data['microformat']['playerMicroformatRenderer']['ownerProfileUrl']
    
    def publishDate(self)->str:
        '''return publish date of video'''
        return self.json_data['microformat']['playerMicroformatRenderer']['publishDate']
    
    def thumbnail(self,quality:int)->str:
        '''
        takes qualist as argumnt by given number
        get thumbnail link by quality:)\n
        ultra-low---> 1\n
        low---------> 2\n
        medium-----> 3\n
        high--------> 4\n
        ultra-high--> 5\n
        '''
        thumbnial_data=self.json_data['videoDetails']['thumbnail']['thumbnails']
        quality=n if not quality<=(n:=len(thumbnial_data)) else quality
        data=thumbnial_data[quality-1]
        return data['url']
    
class PlayList:
    def __init__(self,ytInitialData:json,ytcfg_api):
        '''gathering _info_to_work_with_playlist
            takes ytInitialData json and ytcfg_api tple'''
        self.json_data=ytInitialData
        self.ytcfg_api=ytcfg_api
        self.continues_token=None
        self._size_of_playlist=None
        self._playlist_name=None
        self.json_working_data=self._inisial_working_data()
        
    def _check_for_continues(self)->bool:
        '''check for continues if playlist have more video or not becouse 
            playlist only give first 100 videos and after that we need to 
            request for more so for checking if more video available or not
            we check for continues :)'''
        data=self.json_working_data[-1].get('continuationItemRenderer',None)
        if data:
            #if we find continues we takes the continues token to making post request
            try:self.continues_token=data['continuationEndpoint']['continuationCommand']['token']
            except(KeyError, IndexError):self.continues_token=None
            return bool(data)
        else:
            self.continues_token=None
            return False
    
    def _continues_token(self)->str:
        '''geting continues token'''
        if self.continues_token:
            return self.continues_token
        
        _=self._check_for_continues()
        return self.continues_token
    
    def _build_continuation_url(self, continuation: str) -> tuple[str, dict, dict]:
        '''by using ytctg tuple data that it's get try to make continues_url
            return continues url[0], return header [1] return dict with nessessry info [2]'''
        return (
            (f"https://www.youtube.com/youtubei/{str(self.ytcfg_api[2] if self.ytcfg_api[2] else 'v1')}/browse?key={str(self.ytcfg_api[0])}"),
            {"X-YouTube-Client-Name":str(self.ytcfg_api[4]if self.ytcfg_api[4] else '1'),"X-YouTube-Client-Version":str(self.ytcfg_api[1]if self.ytcfg_api[5]==None else self.ytcfg_api[5]),},
            {"continuation": continuation,"context": {"client": {
                "clientName": str(self.ytcfg_api[3]) if self.ytcfg_api[3] else 'WEB',
                "clientVersion": str(self.ytcfg_api[5]if self.ytcfg_api[1]==None else self.ytcfg_api[1])}}}
            )
    
    def _post_request(self,url, extra_headers=None, data=None, timeout=None)->dict:
        '''making request and returning what we get by that request in json format 
            it coude be bad request 404 or json data containing more video info 
            for perventing bad request we adding extra header info extra_headers.update({"Content-Type": "application/json"})
            if there is more video in playlist and we make request then we get 404 bad request error else we get data'''
        if extra_headers is None:extra_headers = {}
        if data is None:data = {}
        
        extra_headers.update({"Content-Type": "application/json"})
        response = requests.post(url, headers=extra_headers, data=json.dumps(data), timeout=timeout)
        return response.json()
    
    def get_size_of_playlist(self)->str|None:
        '''retrun the size of playlist :)'''
        if self._size_of_playlist: return self._size_of_playlist
        try:
            data_to_prosess=self.json_data['header']['playlistHeaderRenderer']
            size = data_to_prosess.get('numVideosText', {}).get('runs', [{}])[0].get('text',None)
            if size is None:size = data_to_prosess.get('stats', [{}])[0].get('runs', [{}])[0].get('text',None)
            if size is None:size = data_to_prosess.get('briefStats', [{}])[0].get('runs', [{}])[0].get('text',None)
            self._size_of_playlist=size
            return self._size_of_playlist
        except Exception:return None
        
    def _extract_video_itmes(self,json_data:list):
        '''extract_video_items from current json_data it's provided'''
        return [content.get('playlistVideoRenderer', {}).get('videoId') for content in json_data if content.get('playlistVideoRenderer', {}).get('videoId')]
    
    def get_title_of_playlist(self)->str|None:
        '''return the title of playlist'''
        if self._playlist_name:return self._playlist_name
        try:name= self.json_data['microformat']['microformatDataRenderer']['title']
        except KeyError:name= self.json_data['sidebar']['playlistSidebarRenderer']['items'][0
            ]['playlistSidebarPrimaryInfoRenderer']['title']['runs'][0]['text']
        except Exception:name= None
        self._playlist_name=name
        return self._playlist_name
    
    def _contines_working_data_extractor(self,json:dict)->dict:
        '''this is for extracting what we got in reponse of continues post to get more video info after 100 video in a playlist json file so this extract data from that :) sorry for bad explanation it's 5am :)'''
        return json['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']
    
    def _inisial_working_data(self):
        '''this is for extracting working_json_file list of video containing dict'''
        if self.json_data is None:return None
        return self.json_data["contents"]["twoColumnBrowseResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"][
            "contents"][0]["itemSectionRenderer"]["contents"][0][
            "playlistVideoListRenderer"]["contents"]
        
    def extract_video_id(self):
        '''return all available video id'''
        '''just combaind all the function to get list of video don't ask me how it's working i done this at night 
        1 to 4 and i don't know how its works just works so i will modify its run time later becouse 
        1st rule of coding if its work don't touch it so yes and yes ill write explanation later'''
        list_of_videoid=self._extract_video_itmes(self.json_working_data)
        while self._check_for_continues():
            link,extra_header,data=self._build_continuation_url(self._continues_token())
            self.json_working_data=self._contines_working_data_extractor(self._post_request(link,extra_header,data))
            list_of_videoid.extend(self._extract_video_itmes(self.json_working_data))
        return list_of_videoid

class YOUTUBE:
    def _remove_whitespace(self,string)->str:
        """Remove all whitespace characters from a string."""
        return string.translate(str.maketrans('', '', ' \t\n\r\f'))
    
    #about this code we will are thinking to replase upper one but this 
    #line of code still in debate and test also have to make it effectiev
    #for time complexity and space complexity need to improve that tho 
    #it's still have time and space complexity of o(n)
    def _remove_whitespace(self,string)->str:
        output=''
        remove=True
        for i in string:
            if i=='"':
                if remove:remove=False
                else:remove=True
            if remove:
                if i in ' \t\n\r\f':
                    continue
            output+=i
        return output
    
    def _varify_json_format(self,html_data:str,starting_index:int)->dict|None:
        '''This function verifies JSON format within a string.'''
        '''Step 1: It checks the opening curly bracket to start searching for JSON data. If:
            - The character at the starting index is '{', it proceeds.
            - The character at the starting index is '(' or '=' and the next character is '{', it adjusts the string.
        Step 2: It tries to extract JSON data from the string.
            - It iterates through each character in the string, counting opening(+) and closing curly brackets(-) if count become 0 , it marks the end of JSON data.
        Step 3: It attempts to load the extracted JSON data.
            - If successful, it returns the JSON object. If it encounters a JSON decoding error, it returns None.
            time complexity O(n + k) space complexity is O(1) and for json o(k)'''
        counting_curly_bracket=0
        #step 1
        if html_data[starting_index]=='{':pass
        elif html_data[starting_index]=='('and html_data[starting_index+1]=='{':html_data=html_data[1:]
        elif html_data[starting_index]=='='and html_data[starting_index+1]=='{':html_data=html_data[1:]
        else:return None
        # step 2
        for num,i in enumerate(html_data[starting_index:]):
            if i=='{':
                counting_curly_bracket+=1
            elif i=='}':
                counting_curly_bracket-=1
            if counting_curly_bracket==0:
                ending_index=num
                break
        # step 3
        json_data=html_data[starting_index:starting_index+ending_index+1]
        try:return json.loads(json_data)
        except json.JSONDecodeError:return None
    
    def _finding_data(self,html_data:str,search:str)->int|None:
        '''This function finds the word in a document and returns its index.\nIt takes two arguments:
        the string to search in and the word to search.\nreturn index'''
        '''It iterates through the characters of the string, comparing them with the characters of the word
        If a match is found, it increments the index counter If length of the word and index counter is equal return index else none
            time complexity of O(n) and a space complexity o(1)'''
        index=0
        length=len(search)
        for num,item in enumerate(html_data,start=0):
            if item==search[index]:index+=1
            else:index=0
            if index==length:
                return num+1
        return None
    
    def _getting_data(self,html_data:str,search)->dict|None:
        '''This function returns searched data if found, otherwise returns None. It takes the entire string and the search word as arguments.'''
        '''In the first line, it tries to find the index of the first matched object in an HTML document, starting from index 0. 
        After that, it checks if it finds any match. If index_found is None, it simply returns None; otherwise, it passes the value
        to the third line, where it attempts to determine if the matched object belongs to a JSON file. If yes, it returns the JSON object;
        otherwise, it increases the index to the index_found by adding them and searches again. If, during this process, it finds JSON data,
        it returns it.'''
        index=0
        while True:
            index_fond=self._finding_data(html_data[index:],search)
            if index_fond is None:return None
            data=self._varify_json_format(html_data[index:],index_fond)
            if not data:index+=index_fond
            else:return data
            
    def _verify_youtube_link(self,link: str) -> str | None:
        '''verify youtube link and return simple link if link not valid raise link not valid return none'''
        playlist_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:playlist\?list=|playlist\/))([a-zA-Z0-9_-]+)'
        video_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)'
        shorts_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/shorts/)([a-zA-Z0-9_-]+)'
        
        playlist_match = re.match(playlist_regex, link)
        if playlist_match:return "https://www.youtube.com/playlist?list="+playlist_match.group(1),"playlist"
        video_match = re.match(video_regex, link)
        if video_match:return "https://www.youtube.com/watch?v="+video_match.group(1),"video"
        shorts_match = re.match(shorts_regex, link)
        if shorts_match:return "https://www.youtube.com/shorts/"+shorts_match.group(1),"shorts"
        return None
    
    def ytInitialPlayerResponse(self,html_data)->dict|None:
        '''geting ytInitialPlayerResponse json data'''
        search='ytInitialPlayerResponse'
        return self._getting_data(html_data,search=search)
    
    def ytInitialData(self,html_data)->dict|None:
        '''geting ytInitialData json data'''
        search='ytInitialData'
        return self._getting_data(html_data,search=search)
    
    def ytcfg(self,html_data)->dict|None:
        '''getting ytcfg json data'''
        search='ytcfg.set'
        return self._getting_data(html_data,search=search)
    
    def extracting_nessData_for_continution(self,ytcfg_data)->dict:
        '''extracting nessesry info regading ytcfg_data'''
        '''for making request to get more data of playlist 
            becouse a playlist only give 100 video for getting
            more we nned to make request....................'''
        data=(
            ytcfg_data.get('INNERTUBE_API_KEY',None),
            ytcfg_data.get('INNERTUBE_CLIENT_VERSION',None),
            ytcfg_data.get('INNERTUBE_API_VERSION',None),
            ytcfg_data.get('clientName',None),
            ytcfg_data.get('INNERTUBE_CONTEXT_CLIENT_NAME',None),
            ytcfg_data.get('INNERTUBE_CONTEXT_CLIENT_VERSION',None)
        )
        return data
    def __init__(self,link):
        '''gathering html content of youtube link takes link as argumnent'''
        #checking if link is valid or not if not raise error - YouTubeLinkError
        self.link,type=self._verify_youtube_link(link)
        if self.link:pass
        else:raise YouTubeLinkError('youtube link is not valid plese check again or else if link is currect contact akki instagram @akki_raj_._ or @its_just_me_akki')
        
        #checking if provided link contain any info or not if do extract extract html content else raise ConnectionError
        try:data=requests.get(self.link)
        except requests.exceptions.ConnectionError:raise ConnectionError('Please check your connection')
        html_data=data.content.decode('utf-8') if data.status_code==200 else None
        if not html_data:raise YouTubeLinkError('there is some error while collecting youtube data check internet conection or contact code dev instagram- @akki_raj_._ or @its_just_me_akki')
        
        #collecting ytcgf data and by that it's required data else provide none
        html_data=self._remove_whitespace(html_data)
        ytcfg_data=self.ytcfg(html_data)
        if ytcfg_data:
            ytcfg_api=self.extracting_nessData_for_continution(ytcfg_data)
        else:ytcfg_api=(None,None,None,None,None,None)
        
        #inheriting 2 classess in main class\
        if type is None:
            raise YouTubeLinkError('link is not valid')
        elif type=='playlist':
            self.playlist=PlayList(self.ytInitialData(html_data),ytcfg_api)
        elif type=='video' or type=='shorts':
            self.YouTube=YouTube(self.ytInitialPlayerResponse(html_data))

