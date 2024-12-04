import requests
import re
import json
'''
code writer: akhand raj (akki ^^)

contact info:-
    - email id  : akhandraj764@gmail.com
    - git hub   : https://github.com/Akkiraj1234
    - leet code : https://leetcode.com/akhand_raj/

social media:- 
    - instagram : https://www.instagram.com/akki_raj_._
    - instagram : https://www.instagram.com/its_just_me_akki/
'''
class YouTubeLinkError(Exception):
    """
    Error raised for invalid YouTube links.

    This exception is raised when a provided YouTube link is invalid.
    If the link is incorrect, please double-check it. If the link is
    correct but still raises this error, you may contact Akki on Instagram
    at @akki_raj_._ or @its_just_me_akki for further assistance.

    Attributes:
        message (str): A custom error message indicating the reason for the exception.
    """
    def __init__(self, message='youtube link is not valid plese check again or else if link is currect contact akki instagram @akki_raj_._ or @its_just_me_akki'):
        self.message = message
        super().__init__(self.message)



class YouTube:
    """
    Class to extract information from YouTube video data.

    This class takes the `ytInitialPlayerResponse` JSON data as input
    and provides methods to extract various information about the video.

    Args:
        ytInitialPlayerResponse (json): JSON data containing video details.

    Methods:
        streaming_data(): Return the streaming data of the YouTube video.
        
        title(): Return the title of the YouTube video.
        
        artist_name(): Return the artist or channel name of the YouTube video.
        
        length_sec(): Return the length of the video in seconds.
        
        length_millisecond(): Return the length of the video in milliseconds.
        
        video_id(): Return the video ID of the YouTube video.
        
        view_count(): Return the view count of the YouTube video.
        
        artist_channel_link(): Return the link to the artist or channel's YouTube channel.
        
        publish_date(): Return the publish date of the YouTube video.
        
        thumbnail(quality: int): Return the URL of the video thumbnail based on the specified quality.

    Note:
        Thumbnail quality levels:
        - ultra-low: 1
        - low: 2
        - medium: 3
        - high: 4
        - ultra-high: 5
    """

    def __init__(self, ytInitialPlayerResponse: json):
        '''takes ytInitialPlayerResponse JSON data as argument'''
        self.json_data = ytInitialPlayerResponse
        
    def streaming_data(self) -> json:
        '''Return streaming data of the YouTube video.'''
        return self.json_data.get("streamingData", None)
    
    def title(self) -> str:
        '''Return title of the YouTube video.'''
        return self.json_data['videoDetails']['title']

    def artist_name(self) -> str:
        '''Return artist name or channel name of the YouTube video.'''
        return self.json_data['videoDetails']['author']
    
    def length_sec(self) -> int:
        '''Return length of the video in seconds.'''
        return int(self.json_data['videoDetails']['lengthSeconds'])
    
    def length_millisecond(self) -> int:
        '''Return length of the video in milliseconds.'''
        return int(self.json_data['videoDetails']['lengthSeconds']) * 1000
    
    def video_id(self) -> str:
        '''Return video ID of the YouTube video.'''
        return self.json_data['videoDetails']['videoId']
    
    def view_count(self) -> int:
        '''Return views of the video.'''
        return int(self.json_data['videoDetails']['viewCount'])
    
    def artist_channel_link(self) -> str:
        '''Return the link of the artist's or channel's YouTube channel.'''
        return self.json_data['microformat']['playerMicroformatRenderer']['ownerProfileUrl']
    
    def publish_date(self) -> str:
        '''Return publish date of video.'''
        return self.json_data['microformat']['playerMicroformatRenderer']['publishDate']
    
    def thumbnail(self, quality: int) -> str:
        '''
        Return the URL of the video thumbnail based on the specified quality.

        Args:
            quality (int): The quality level of the thumbnail.
                Available options: 1 (ultra-low), 2 (low), 3 (medium), 4 (high), 5 (ultra-high).
        '''
        thumbnail_data = self.json_data['videoDetails']['thumbnail']['thumbnails']
        quality = n if not quality <= (n := len(thumbnail_data)) else quality
        data = thumbnail_data[quality - 1]
        return data['url']
    
    
    

class PlayList:
    """
    Class for extracting information from YouTube playlist data.

    This class is designed to work with YouTube playlist data and provides methods to retrieve
    various details such as the size of the playlist, the title of the playlist, and the video IDs
    of all videos in the playlist.

    Args:
        ytInitialData (json): JSON data containing playlist details.
        ytcfg_api (tuple): Tuple containing YouTube API configuration details.

    Attributes:
        json_data (json): JSON data containing playlist details.
        ytcfg_api (tuple): Tuple containing YouTube API configuration details.
        continues_token (str): Token for retrieving more videos in case of pagination.
        _size_of_playlist (str): Size of the playlist.
        _playlist_name (str): Name of the playlist.
        json_working_data (list): Initial working JSON data for extracting video details.

    Methods:
        _check_for_continues(): Check if there are more videos in the playlist.
        _continues_token(): Get the continuation token for pagination.
        _build_continuation_url(continuation: str) -> tuple: Build the URL, headers, and data for continuation request.
        _post_request(url, extra_headers=None, data=None, timeout=None) -> dict: Make a POST request and return JSON response.
        get_size_of_playlist() -> str|None: Get the size of the playlist.
        _extract_video_items(json_data: list) -> list: Extract video IDs from JSON data.
        get_title_of_playlist() -> str|None: Get the title of the playlist.
        _continues_working_data_extractor(json: dict) -> dict: Extract data from continuation response.
        _initial_working_data(): Extract initial working JSON data from the playlist.

    Note:
        - This class supports pagination to retrieve all videos in the playlist.
        - Pagination is handled internally to gather all available video IDs.
    """

    def __init__(self,ytInitialData:json,ytcfg_api):
        '''gathering _info_to_work_with_playlist
            takes ytInitialData JSON and ytcfg_api tuple'''
        self.json_data=ytInitialData
        self.ytcfg_api=ytcfg_api
        self.continues_token=None
        self._size_of_playlist=None
        self._playlist_name=None
        self.json_working_data=self._inisial_working_data()
        
    def _check_for_continues(self)->bool:
        '''
        Check if the playlist has more videos.

        This method checks if there are more videos available in the playlist beyond the first 100.
        YouTube playlists have a limit of displaying only the first 100 videos, so if there are more
        videos in the playlist, a continuation token is provided to fetch additional videos.

        Returns:
            bool: True if more videos are available in the playlist, False otherwise.
        '''
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
        '''
        Get the continuation token.

        This method retrieves the continuation token required for fetching additional videos
        beyond the first 100 in a playlist.

        Returns:
            str: The continuation token if available, otherwise an empty string.
        '''
        if self.continues_token:
            return self.continues_token
        
        _=self._check_for_continues()
        return self.continues_token
    
    def _build_continuation_url(self, continuation: str) -> tuple[str, dict, dict]:
        '''
        Build the URL, headers, and data for fetching additional videos in the playlist.

        This method constructs the URL, headers, and data required for making a POST request
        to fetch additional videos in a playlist beyond the first 100.

        Args:
            continuation (str): The continuation token for pagination.

        Returns:
            tuple: A tuple containing the following:
                - str: The URL for the continuation request.
                - dict: Headers for the continuation request.
                - dict: Data for the continuation request containing necessary information.
        '''
        # Constructing the URL
        url = f"https://www.youtube.com/youtubei/{str(self.ytcfg_api[2] if self.ytcfg_api[2] else 'v1')}/browse?key={str(self.ytcfg_api[0])}"
        
        # Constructing the headers
        headers = {
            "X-YouTube-Client-Name": str(self.ytcfg_api[4] if self.ytcfg_api[4] else '1'),
            "X-YouTube-Client-Version": str(self.ytcfg_api[1] if self.ytcfg_api[5] == None else self.ytcfg_api[5]),
        }
        
        # Constructing the data
        data = {
            "continuation": continuation,
            "context": {
                "client": {
                    "clientName": str(self.ytcfg_api[3]) if self.ytcfg_api[3] else 'WEB',
                    "clientVersion": str(self.ytcfg_api[5] if self.ytcfg_api[1] == None else self.ytcfg_api[1])
                }
            }
        }

        return url, headers, data
    
    def _post_request(self,url, extra_headers=None, data=None, timeout=None)->dict:
        '''
        Make a POST request and return the response in JSON format.

        This method makes a POST request to the specified URL with optional extra headers and data.
        It returns the response obtained from the request in JSON format.

        Args:
            url (str): The URL to make the POST request.
            extra_headers (dict, optional): Additional headers to include in the request. Defaults to None.
            data (dict, optional): Data to include in the request body. Defaults to None.
            timeout (float, optional): Timeout for the request in seconds. Defaults to None.

        Returns:
            dict: The JSON response obtained from the request.

        Note:
            - If there are more videos in the playlist and a request is made, a 404 error may occur if
            the pagination token is not provided correctly.
        '''
        
        if extra_headers is None:
            extra_headers = {}
            
        if data is None:
            data = {}
        
        extra_headers.update({"Content-Type": "application/json"})
        response = requests.post(url, headers=extra_headers, data=json.dumps(data), timeout=timeout)
        return response.json()
    
    def get_size_of_playlist(self)->str|None:
        '''
        Get the size of the playlist.

        This method retrieves the size of the playlist, indicating the number of videos it contains.

        Returns:
            str | None: The size of the playlist as a string if available, otherwise None.
        '''
        if self._size_of_playlist: 
            return self._size_of_playlist
        
        try:
            data_to_prosess=self.json_data['header']['playlistHeaderRenderer']
            size = data_to_prosess.get('numVideosText', {}).get('runs', [{}])[0].get('text',None)
            
            if size is None:
                size = data_to_prosess.get('stats', [{}])[0].get('runs', [{}])[0].get('text',None)
            if size is None:
                size = data_to_prosess.get('briefStats', [{}])[0].get('runs', [{}])[0].get('text',None)
                
            self._size_of_playlist=size
            
            return self._size_of_playlist
        except Exception:
            return None
        
    def _extract_video_itmes(self,json_data:list):
        '''
        Extract video items from the provided JSON data.

        This method extracts video IDs from the current JSON data provided.

        Args:
            json_data (list): The JSON data containing video information.

        Returns:
            list: A list of video IDs extracted from the JSON data.

        Note:
            The method filters out non-playlist video renderer items and extracts their corresponding video IDs.
        '''
        return [content.get('playlistVideoRenderer', {}).get('videoId') for content in json_data if content.get('playlistVideoRenderer', {}).get('videoId')]
    
    def get_title_of_playlist(self)->str|None:
        '''
        Get the title of the playlist.

        This method retrieves the title of the playlist.

        Returns:
            str | None: The title of the playlist if available, otherwise None.
        '''
        
        if self._playlist_name:
            return self._playlist_name
        
        try:
            name= self.json_data['microformat']['microformatDataRenderer']['title']
        except KeyError:
            name= self.json_data['sidebar']['playlistSidebarRenderer']['items'][0
            ]['playlistSidebarPrimaryInfoRenderer']['title']['runs'][0]['text']
        except Exception:
            name= None
            
        self._playlist_name=name
        return self._playlist_name
    
    def _contines_working_data_extractor(self,json:dict)->dict:
        '''
        Extract continuation items from the response of a continues post request.

        This method extracts continuation items from the response of a continues post request,
        which retrieves more video information after the first 100 videos in a playlist JSON file.

        Args:
            json (dict): The JSON response containing continuation items.

        Returns:
            dict: The continuation items extracted from the JSON response.

        Note:
            This method is specifically designed to extract continuation items from the JSON
            response structure expected from a continues post request in the context of retrieving
            additional video information for a playlist.
        '''
        return json['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']
    
    def _inisial_working_data(self):
        '''
        Extract initial working data from the provided JSON data.

        This method extracts the initial working data, which is a list of dictionaries containing
        video information, from the provided JSON data.

        Returns:
            list | None: The initial working data if available, otherwise None.

        Note:
            The initial working data is extracted from a specific structure within the JSON data.
            If the JSON data is None, None is returned.
        '''
        if self.json_data is None:
            return None
        
        return self.json_data["contents"]["twoColumnBrowseResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"][
            "contents"][0]["itemSectionRenderer"]["contents"][0][
            "playlistVideoListRenderer"]["contents"]
        
    def extract_video_id(self):
        '''
        Retrieve all available video IDs from the playlist.

        This method retrieves a list of all available video IDs within the playlist.
        It iterates through the playlist JSON data, extracting video IDs, and handles
        continuation tokens to ensure complete retrieval of video IDs, even beyond the
        initial 100 videos.

        Returns:
            list: A list containing all available video IDs within the playlist.

        Usage:
            1. Create an instance of the PlayList class.
            2. Call the extract_video_id() method on the instance to retrieve the video IDs.

            Example:
            >>> playlist_instance = PlayList(ytInitialData, ytcfg_api)
            >>> video_ids = playlist_instance.extract_video_id()
            >>> print(video_ids)

        Note:
            The method iterates through the JSON data and handles continuation tokens to ensure
            all video IDs are retrieved, even beyond the initial 100 videos.

        '''
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
    """
    A class representing the YouTube platform.

    This class provides functionalities to interact with YouTube content such as playlists, videos, and shorts.
    It allows for extracting JSON data, verifying YouTube links, and initializing playlist or video objects based on the provided link.

    Attributes:
        link (str): The YouTube link provided during initialization.

    Methods:
        _remove_whitespace(string: str) -> str:
            Remove all whitespace characters from a string, except those within double quotes.

        _varify_json_format(html_data: str, starting_index: int) -> dict | None:
            Verify JSON format within a string.

        _finding_data(html_data: str, search: str) -> int | None:
            Find the word in a document and return its index.

        _getting_data(html_data: str, search) -> dict | None:
            Return searched data if found, otherwise return None.

        _verify_youtube_link(link: str) -> str | None:
            Verify YouTube link and return a simple link.

        ytInitialPlayerResponse(html_data: str) -> dict | None:
            Get ytInitialPlayerResponse JSON data.

        ytInitialData(html_data: str) -> dict | None:
            Get ytInitialData JSON data.

        ytcfg(html_data: str) -> dict | None:
            Get ytcfg JSON data.

        extracting_nessData_for_continution(ytcfg_data: dict) -> dict:
            Extract necessary information from ytcfg_data for continuation.

        __init__(link: str):
            Initialize a YouTube object with the provided link.
    """
    def _remove_whitespace(self,string)->str:
        """Remove all whitespace characters from a string."""
        return string.translate(str.maketrans('', '', ' \t\n\r\f'))
    
    # This code snippet is currently under consideration for replacement with the code above.
    # Although this line of code is still being debated and tested, we also need to ensure
    # its effectiveness in terms of time complexity and space complexity. However, it still
    # has a time and space complexity of O(n).
    def _remove_whitespace(self, string: str) -> str:
        """
        Remove all whitespace characters from a string, except those within double quotes.

        This method removes all whitespace characters from the input string, except those
        within double quotes. It preserves whitespace characters that are enclosed within
        double quotes. This can be useful, for example, when extracting text from HTML
        documents where whitespace within certain elements like titles should be preserved.

        Parameters:
            string (str): The input string from which whitespace characters are to be removed.

        Returns:
            str: The modified string with whitespace characters removed, except those within
                double quotes.

        Example:
            >>> instance = ClassName()
            >>> modified_string = instance._remove_whitespace('This is "a string" with whitespace.')
            >>> print(modified_string)
            Thisis"a string"withwhitespace.

        Note:
            This method only removes whitespace characters outside of double quotes. Whitespace
            within double quotes is preserved in the output.
        """
        output = ''
        remove = True
        for char in string:
            if char == '"':
                remove = not remove #if true then became false if false then beacme true
            if remove:
                if char in ' \t\n\r\f':
                    continue #continue to the main loop and so it's don't write whitespace in output
            output += char
        return output

    
    def _varify_json_format(self,html_data:str,starting_index:int)->dict|None:
        """
        Verify JSON format within a string.

        Steps:
        1. Check the opening curly bracket to start searching for JSON data. If:
            - The character at the starting index is '{', it proceeds.
            - The character at the starting index is '(' or '=' and the next character is '{', it adjusts the string.
        2. Extract JSON data from the string by iterating through each character, counting opening (+) and closing (-)
        curly brackets. When the count becomes 0, it marks the end of JSON data.
        3. Attempt to load the extracted JSON data. If successful, return the JSON object.
        If it encounters a JSON decoding error, return None.

        Args:
        - html_data (str): The string containing HTML data.
        - starting_index (int): The index to start searching for JSON data.

        Returns:
        - dict | None: The JSON object if successful, otherwise None.

        Time complexity: O(n + k), where n is the length of the string and k is the length of the extracted JSON data.
        Space complexity: O(1) for the function, O(k) for the JSON data."""
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
        """
        Find the word in a document and return its index.

        Args:
        - html_data (str): The string to search in.
        - search (str): The word to search for.

        Returns:
        - int | None: The index of the word if found, otherwise None.

        It iterates through the characters of the string, comparing them with the characters of the word.
        If a match is found, it increments the index counter. If the length of the word and the index counter is equal,
        return the index; otherwise, return None.

        Time complexity: O(n)
        Space complexity: O(1)
        """
        index=0
        length=len(search)
        for num,item in enumerate(html_data,start=0):
            if item==search[index]:
                index+=1
            else:
                index=0
                
            if index==length:
                return num+1
        return None
    
    def _getting_data(self,html_data:str,search)->dict|None:
        """
        Return searched data if found, otherwise return None.

        Args:
        - html_data (str): The entire string containing the data.
        - search (str): The search word.

        Returns:
        - dict | None: The searched data if found, otherwise None.

        It tries to find the index of the first matched object in an HTML document, starting from index 0.
        If no match is found, it returns None. If a match is found, it checks if the matched object belongs to a JSON file.
        If it is JSON, it returns the JSON object; otherwise, it increases the index to the index found and searches again.
        If JSON data is found during this process, it returns it.

        """
        index=0
        while True:
            index_fond=self._finding_data(html_data[index:],search)
            if index_fond is None:
                return None
            
            data=self._varify_json_format(html_data[index:],index_fond)
            if not data:
                index+=index_fond
            else:
                return data
            
    def _verify_youtube_link(self,link: str) -> str | None:
        """
        Verify YouTube link and return a simple link.

        Args:
        - link (str): The YouTube link to verify.

        Returns:
        - str | None: The verified link if valid, otherwise None.

        If the link is a valid playlist link, it returns the complete link with 'playlist' as the type.
        If the link is a valid video link, it returns the complete link with 'video' as the type.
        If the link is a valid YouTube shorts link, it returns the complete link with 'shorts' as the type.
        If the link is not valid, it returns None.

        """
        playlist_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:playlist\?list=|playlist\/))([a-zA-Z0-9_-]+)'
        video_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)'
        shorts_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/shorts/)([a-zA-Z0-9_-]+)'
        
        playlist_match = re.match(playlist_regex, link)
        if playlist_match:
            return "https://www.youtube.com/playlist?list="+playlist_match.group(1),"playlist"
        
        video_match = re.match(video_regex, link)
        if video_match:
            return "https://www.youtube.com/watch?v="+video_match.group(1),"video"
        
        shorts_match = re.match(shorts_regex, link)
        if shorts_match:
            return "https://www.youtube.com/shorts/"+shorts_match.group(1),"shorts"
        
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
        """
        Extract necessary information from ytcfg_data for continuation.

        This function extracts essential information from the ytcfg_data for making requests to get more data of a playlist,
        as a playlist only gives 100 videos. This extracted information includes the API key, client version, API version, client name,
        and other relevant context.

        Args:
        - ytcfg_data (dict): The ytcfg data to extract information from.

        Returns:
        - dict: A dictionary containing the extracted necessary information.
        
        """
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
        """Initialize a YouTube object with the ytInitialPlayerResponse JSON data extracted from HTML data.

        Parameters:
            html_data (str): The HTML data from which the ytInitialPlayerResponse JSON data will be extracted.

        Returns:
            None
        """
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
