from ..error import StreamdlError
from typing import *
import json
"""
Class to extract information from YouTube video data.

This class takes the `ytInitialPlayerResponse` JSON data as input
and provides methods to extract various information about the video.
"""


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
        """takes ytInitialPlayerResponse JSON data as argument"""
        self.ytInitialPlayerResponse = ytInitialPlayerResponse

    def get_streaming_data(self) -> json:
        '''Return streaming data of the YouTube video.'''
        return self.ytInitialPlayerResponse.get("streamingData", None)

    def title(self) -> str:
        '''Return title of the YouTube video.'''
        return self.ytInitialPlayerResponse['videoDetails']['title']

    def artist_name(self) -> str:
        """Return artist name or channel name of the YouTube video."""
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
        return self.json_data['microformat']['playerMicroformatRenderer'][
            'ownerProfileUrl']

    def publish_date(self) -> str:
        '''Return publish date of video.'''
        return self.json_data['microformat']['playerMicroformatRenderer'][
            'publishDate']

    def thumbnail(self, quality: int) -> str:
        '''
        Return the URL of the video thumbnail based on the specified quality.

        Args:
            quality (int): The quality level of the thumbnail.
                Available options: 1 (ultra-low), 2 (low), 3 (medium), 4 (high), 5 (ultra-high).
        '''
        thumbnail_data = self.json_data['videoDetails']['thumbnail'][
            'thumbnails']

        quality = min(len(thumbnail_data), max(quality, 1))
        data = thumbnail_data[quality - 1]
        return data['url']
