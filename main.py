from tempfile import NamedTemporaryFile
from io import BytesIO
import subprocess
import os

import requests#need to remove request :) and make own function
from PIL import Image # need to remove pil library and it's onlly use to crop can done by ffmpeg :)

from youtube import YOUTUBE
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!important_variables!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
default_path='C:\\Users\\DELL\\Desktop\\side project'
ffmpeg_path='C:\\ffmpeg\\ffmpeg-2024-03-11-git-3d1860ec8d-full_build\\bin\\ffmpeg.exe'
# ffmpeg_path=".\\PyStreamSaver_data\\ffmpeg-2024-03-11-git-3d1860ec8d-full_build\\bin\\ffmpeg.exe"

def logo(clear:bool=True,stop:bool=False)->str:
    '''
    this function print the logo for the script
    
    Parameters:
    - clear = True|False : if true
    then clear the terminal then print the logo \n
    - stop = True|False : if true 
    then after printing the logo it's ask for input(enter)
    before printing anything.
    
    return:
    - str: formated logo of this project by setting we made by Parameters
    '''
    os.system('cls') if clear else None
    print(
        colored ("         |=|           \n",'blue')
        +colored("         |=|          \n",'blue')
        +colored("      ___|=|___\n",'blue')
        +colored("      \\\\=====//",'blue')+colored("  Downloader\n",'yellow')
        +colored("       \\\\===// ",'blue')+colored("  By--------\n",'yellow')
        +colored("        \\\\=//  ",'blue')+colored("  AKKI------\n",'yellow')
        )
    _=input(colored('enter to continue ','blue')) if stop else None
    
    
def colored(string, color):
    """
    Return the input string with specified color in ANSI escape sequence.

    Parameters:
    - string (str): The input string to be colored.
    - color (str): The color name. Supported color names are 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white', 'black', 'gray', and 'reset'.

    Returns:
    - str: The input string wrapped in ANSI escape sequence for the specified color.

    Example:
    >>> colored("Hello, world!", "blue")
    '\x1b[34mHello, world!\x1b[0m'
    """
    colors = {
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'purple': '\x1b[35m',
        'cyan': '\x1b[36m',
        'white': '\x1b[37m',
        'black': '\x1b[30m',
        'gray': '\x1b[90m',
        'reset': '\x1b[0m'
    }
    # Color escape sequences are added before the string and default to white color at the end (\x1b[0m).
    color_code = colors.get(color.lower(), '\x1b[0m')
    return f"{color_code}{string}\x1b[0m"


def custom_progress_bar(current, total, length=60)->str:
    '''
    Generates a custom progress bar representation based on the current progress, total work, and specified length.
    
    PARAMETER:
    - current: Current progress value.
    - total: Total work value.
    - length: Length of the progress bar (default is 60).
    - *also it's requied colored library so from termcolor import colored.

    RETURN:
    - str: A string representing the custom progress bar.
      
    EXAMPLE:
    >>> custom_progress_bar(30, 50)  # Generates a progress bar representing 30% completion
    [=====>                                 ] 30%
    '''
    # The completed progress is represented by '=' characters * 'blocks_completed' times, followed by spaces for the remaining length.
    # The progress bar is updated in-place using '\r', and printed along with the formatted percentage and used colored to color text.
    progress = current / total
    blocks_compleated = int(progress * length)
    bar = colored('[','yellow') + colored('=','blue') * blocks_compleated+colored('>','yellow') + ' ' * (length - blocks_compleated) + colored(']','yellow')
    percentage = colored('{:.0%}'.format(progress),'blue')
    print('\r' + bar + ' ' + percentage, end='', flush=True)


def _valid_name(name:str)->str:
    """
    Return a valid name for creating files and directories in Windows.

    Args:
        name (str): The input name to be validated.

    Returns:
        str: A valid name with illegal characters replaced by underscores.

    Example:
        >>> invalid_name = 'file<>.txt'
        >>> valid_name = _valid_name(invalid_name)
        >>> print(valid_name)
        file____.txt
    """
    return ''.join(a if not a in '<>:"/\\|?*' else '_' for a in name)

def valid_path_name(dir_path,name:str)->str:
    """
    Return a valid filename by modifying it if it already exists in the specified directory path.
    
    Args:
        dir_path (str): The directory path where the file will be saved.
        name (str): The name of the file including its extension.
        
    Returns:
        str: A valid filename with a modified name if the original name already exists in the directory.
        
    Example:
        >>> dir_path = "C:\\Users\\User\\Desktop\\"
        >>> existing_name = "file.txt"
        >>> valid_name = valid_path_name(dir_path, existing_name)
        >>> print(valid_name)
        "C:\\Users\\User\\Desktop\\file(1).txt"
    """
    name,extention=_valid_name(name).rsplit('.', 1)
    number=1
    extra=''
    while os.path.exists(dir_path+'\\'+name+extra+'.'+extention):
        extra=f'({number})'
        number+=1
    return dir_path+'\\'+name+extra+'.'+extention


def valid_dir_name(dir_path:str,name:str)->str:
    """
    Return a valid directory name by modifying it if it already exists in the specified directory path.
    
    Args:
        dir_path (str): The directory path where the directory will be created.
        name (str): The name of the directory.
        
    Returns:
        str: A valid directory name with a modified name if the original name already exists in the directory.
        
    Example:
        >>> dir_path = "C:\\Users\\User\\Desktop\\"
        >>> existing_name = "directory"
        >>> valid_name = valid_dir_name(dir_path, existing_name)
        >>> print(valid_name)
        C:\\Users\\User\\Desktop\\directory(1)
    """
    name=_valid_name(name)
    extra=''
    number=1
    while os.path.exists(dir_path+'\\'+name+extra):
        extra=f'({number})'
        number+=1
    return dir_path+'\\'+name+extra

def crop_center_square(image_path)->None:#need to change it can done by ffmpeg
    """
    Crop the image to center it on a 1:1 aspect ratio.

    Parameters:
    - image_path (str): The path to the image file.

    Returns:
    None. The function directly saves the cropped image back to the original file.

    Example:
    >>> crop_center_square("image.jpg")

    Notes:
    - This function crops the image to make it a square by taking the larger dimension (width or height) and
      cropping from the center to achieve a 1:1 aspect ratio.
    - The input image should be in JPEG format.
    - The function directly modifies the original image file by overwriting it with the cropped version.
    writen by chat-gpt :) just want to let u guys know
    """
    with open(image_path, 'rb') as f:
        image_data = f.read()
    img = Image.open(BytesIO(image_data))
    width, height = img.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    img = img.crop((left, top, right, bottom))
    img.save(image_path)
    
def get_size(content_length)->str:
    """
    Converts the given content_length (in bytes) into a human_readable format.
    
    Parameters:
    - content_length (int): The length of content in bytes.
    
    Returns: 
    - str: A string representing the content length in a human-readable format,
    with units (bytes, KB, MB, GB).
           
    Example:
    >>> get_size(123456789)
    '117.74 MB'
    """
    content_length=int(content_length)
    if content_length >= 1073741824:
        return f"{content_length / 1073741824:.2f} GB"
    elif content_length >= 1048576:
        return f"{content_length / 1048576:.2f} MB"
    elif content_length >= 1024:
        return f"{content_length / 1024:.2f} KB"
    else:
        return f"{content_length} bytes"
    
def sec_to_min_to_hours(sec)->str:
    '''
    Convert time in seconds to minutes or hours.

    Parameters:  sec (int): Time duration in seconds.

    Returns: (str) The time duration converted to minutes or hours, formatted accordingly.

    Example:
    >>> sec_to_min_to_hours(3600)
    '1.00 hours'
    '''
    min=float(sec)/60
    if min<60:time='%.2f min'%min
    else:time='%.2f hours'%(float(min)/60)
    return time

def add_audio_to_video(video_path, audio_path,ffmpeg_path,output_path):
    """
    Add audio to a video using ffmpeg.

    Parameters:
    - video_path (str): The path to the input video file.
    - audio_path (str): The path to the input audio file.
    - ffmpeg_path (str): The path to the ffmpeg executable.
    - output_path (str): The path to save the output video file.
    """
    command = [ffmpeg_path,'-i', video_path,'-i', audio_path,'-c:v', 'copy','-c:a', 'aac','-strict', 'experimental',output_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
def convert_audio(input_file, output_file, ffmpeg_path):
    """
    Convert audio to another format using ffmpeg.

    Parameters:
    - input_file (str or bytes): The input audio file path or bytes data.
    - output_file (str): The path to save the converted audio file.
    - ffmpeg_path (str): The path to the ffmpeg executable.
    """
    command = [ffmpeg_path, '-i', input_file, '-codec:a', 'libmp3lame', output_file]
    subprocess.run(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def add_cover_in_music(audio_file_path:str, title:str, artist:str, cover_photo_url:str,output_path:str,ffmpeg_path:str):
    '''
    Add cover art and metadata to an audio file.

    Parameters:
    - audio_file_path (str): The path to the input audio file.
    - title (str): The title metadata for the audio file.
    - artist (str): The artist metadata for the audio file.
    - cover_photo_url (str): The URL of the cover photo.
    - output_path (str): The path to save the modified audio file.
    - ffmpeg_path (str): The path to the FFmpeg executable.

    This function downloads a cover photo from the provided URL, adds it to the input audio file,
    and sets the specified metadata such as title and artist. The modified audio file is saved
    at the specified output path.

    Example:
    >>> add_cover_in_music("input_audio.mp3", "Song Title", "Artist Name", "cover.jpg", "output_audio.mp3", "/path/to/ffmpeg")
    '''
    temp_file=NamedTemporaryFile(delete=False,suffix='.jpeg')
    download_file_with_resume(cover_photo_url,temp_file.name)
    crop_center_square(temp_file.name)
    comand=[ffmpeg_path, '-i', audio_file_path, '-i', temp_file.name,'-c','copy', '-map', '0', '-map', '1', '-metadata', f'title={title}', '-metadata', f'artist={artist}', output_path]
    subprocess.call(comand,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    temp_file.close()
    os.unlink(temp_file.name)
    
    
def _add_cover_and_meta_data(input_data,output_path,ffmpeg_path,title, artist, cover_photo_url):
    '''
    Convert input audio data to MP3 format, add cover art and metadata, and save the modified audio file.

    Parameters:
    - input_data (str or bytes): The input audio data path or bytes.
    - output_path (str): The path to save the modified audio file.
    - ffmpeg_path (str): The path to the FFmpeg executable.
    - title (str): The title metadata for the audio file.
    - artist (str): The artist metadata for the audio file.
    - cover_photo_url (str): The URL of the cover photo.

    This function converts the input audio data to MP3 format using FFmpeg, downloads the cover photo from the provided URL,
    adds it along with the specified metadata (title and artist) to the audio file, and saves the modified audio file
    at the specified output path. The temporary files created during the process are automatically deleted.

    Example:
    >>> _add_cover_and_meta_data("input_audio.wav", "output_audio.mp3", "/path/to/ffmpeg", "My Title", "My Artist", "cover_photo_url.jpg")
    '''
    temp_file='output.mp3'
    convert_audio(input_data,temp_file,ffmpeg_path)
    add_cover_in_music(temp_file,title,artist,cover_photo_url,output_path,ffmpeg_path)
    os.unlink(temp_file)
    

def download_file_with_resume(url, filename, retry=1,downloaded_bytes=0):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  fix it when i will make my own request library 
    try:
        headers = {'Range': f'bytes={downloaded_bytes}-'}
        response = requests.get(url, headers=headers, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        custom_progress_bar(downloaded_bytes, total_size)
        with open(filename, 'ab') as f:
            for chunk in response.iter_content(chunk_size=4096):
                if not chunk: continue
                f.write(chunk)
                downloaded_bytes += len(chunk)
                custom_progress_bar(downloaded_bytes, total_size)
        print()
        return True
    except Exception:return None


def handeking_error_while_downloading_music(dict1,quality:str,mime_type,output_path,attempt_to_download=1):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! same fix when i will make my own request library
    quality=quality if quality.isdigit() else '3'
    for _ in range(attempt_to_download):
        link_audio=get_audio_link_quality(dict1,quality,mime_type)[0]
        response=download_file_with_resume(link_audio,output_path)
        if response:return True
        else:
            mime_type = 'opus' if mime_type=='mp3' else 'mp3' if 3-attempt_to_download==0 else'opus'
            quality = '1' if int(quality)>3 else '2'if quality !='2' else '3'
            with open(output_path,'wb')as f:f.write(b'')
    return False


def get_video_info(youtube_onj:YOUTUBE)->dict|None:
    '''gather the video info from YOUTUBE.youtube.streaming_data() and store them in 
    a dict and return the dict takes youtube_obj as an arguemnt
    
    PARAMETERS:
    - takes youtube obj as an argument
    
    RETURNS: 
    - returns a dict by gathering info from streming data 
    
    STRUCTURE OF DICT
    >>> dict1={'video':{'audio_aviable':{},'mp4':{},'webm':{}},'music':{'mp3':{},'opus':{}}}
    
    EXAMPLE: 
    >>> from youtube import YOUTUBE
    >>> youtube_obj=YOUTUBE("www.youtube.com/watch=?123ertfdd")
    >>> dict1= get_video_info(youtube_obj)
    '''
    streaming_data=youtube_onj.YouTube.streaming_data()
    if streaming_data is None:return None
    # trying to gather 'url' from streaming_data becouse if youtube content is 18+
    # link came encoded with there token so we can't gather 'url' will return none
    if streaming_data['formats'][0].get('url',None) is None:return None
    
    # Initialize the dictionary to store video info
    dict1={'video':{'audio_aviable':{},'mp4':{},'webm':{}},'music':{'mp3':{},'opus':{}}}
    
    #tring to gather content lenth by differnt aproach 
    for data in streaming_data['formats']:
        try:size=data['contentLength']
        except Exception:size=data['bitrate']*(int(data['approxDurationMs'])/10000)
        dict1['video']['audio_aviable'].update({data['qualityLabel']:(data['url'],size)})
    
    # Iterate through each format in streaming data to gather video and audio info
    for data in streaming_data['adaptiveFormats']:
        mimetype=data['mimeType']
        if 'video/mp4' in mimetype:
            dict1['video']['mp4'].update({data['qualityLabel']:(data['url'],data['contentLength'])})
        elif 'video/webm' in mimetype:
            dict1['video']['webm'].update({data['qualityLabel']:(data['url'],data['contentLength'])})
        elif 'audio/mp4' in mimetype:
            dict1['music']['mp3'].update({data['contentLength']:(data['url'],data['audioQuality'])})
        elif 'audio/webm':
            dict1['music']['opus'].update({data['contentLength']:(data['url'],data['audioQuality'])})
    return dict1

def get_video_link_by_resulation(dict1,resulation,mime_type='mp4')->tuple|None:
    '''
    Returns the video link by given resolution and MIME type. If the provided resolution is not available,
    it tries to return the closest available resolution. If no suitable video link is found, returns None.
    
    PARAMETER: 
    - dict1 : Takes a dictionary containing streaming data info. Example:
              dict1 = get_video_info(python_obj)
    - resolution : Specifies the resolution of the video. Provide resolutions in the format: '2160p60', '2160p', 
                   '1440p60', '1440p', '1080p60', '1080p', '720p60', '720p', '480p60', '480p', '360p', '240p', '144p'.
    - mime_type : Specifies the MIME type of the video. If MIME type is not valid or not in the list ('mp4', 'webm'), 
                  it will default to 'mp4'.
    
    RETURN: 
    - tuple: Tuple containing the link of the video, a boolean indicating whether audio is merged with video, 
             the actual resolution of the video, and the MIME type. Returns None if no suitable video link is found.
    
    STRUCTURE:
    >>> tuple_containing = (('url' : str , 'contentLength' : str),'audio_merged': bool, 'resolution': str, 'mime_type': str)
    
    EXAMPLE:
    >>> dict1 = get_video_info(youtube_obj)
    >>> link = get_video_link_by_resolution(dict1, '720p')
    >>> request.get(link[0][0])
    '''
    list_of_resulation=('2160p60','2160p','1440p60','1440p','1080p60','1080p','720p60','720p','480p60','480p','360p','240p','144p')
    mime_type='mp4'if mime_type not in ('mp4','webm') else mime_type #changing if not giving curectly
    resulation='360p' if resulation not in list_of_resulation else resulation# changing if not provided curectly
   
    # Adjusting MIME type based on availability in the provided data (if not able to get mime type change it to mp3 if it was webm and if webm then mp3)
    mime_type = mime_type if dict1['video'].get(mime_type) is not None else 'mp4' if mime_type == 'webm' else 'webm'
    
    #checking if webm is availbale or not if not checking for audio_aviableity is available or not if not then set default data becouse 'mp3' 360p data will alway be collected
    if dict1['video'][mime_type]is None:
        if dict1['video']['audio_aviable'] is None:return None
        else:mime_type='mp4';resulation='360p'
    
    #trying get data which have audio if resualtion 360p or 720p selected
    if mime_type=='mp4' and (resulation=='360p' or resulation=='720p'):
        data=dict1['video']['audio_aviable'].get(resulation)
        if data is not None:return data,True,resulation,mime_type
    
    # trying to gather data if above is turns falase or else resualtion differnt check both possiblity exaple 720p or 720p60
    for i in (resulation+'60',resulation):
        data=dict1['video'][mime_type].get(i)
        if data is not None:return data,False,i,mime_type
    
    #at last trying to get any lower resualtion that availabe in dict1 by going true each value in list_of_resulation andn at last if not found any return  none
    list_of_resulation=list_of_resulation[list_of_resulation.index(resulation):]
    for i in list_of_resulation:
        data=dict1['video'][mime_type].get(i)
        if data is not None:return data,False,i,mime_type
    return None

def get_audio_link_quality(dict1,quality:str,mime_type)->tuple|None:
    '''
    Returns a tuple containing audio link and audio quality by given parameters. 
    If the audio link does not match the given parameter, it tries to return lower quality.
    
    PARAMETER: 
    - dict1 : Takes a dictionary containing streaming data info. Example:
              dict1 = get_video_info(python_obj)
    - quality : Takes quality as argument in given options:
                1 for lowest, 2 for medium, and 3 for higher.
    - mime_type : Specifies the MIME type of the video you want to get. If MIME type is not valid
                  or not in the list, it will default to mp4.
    
    RETURN: 
    - tuple: Tuple containing link of the video and audio quality, else None
    
    STRUCTURE:
    >>> tuple_containing = ('url': str, 'audio_quality': str)
    
    EXAMPLE:
    >>> dict1 = get_video_info(youtube_obj)
    >>> link = get_audio_link_quality(dict1, '2', 'mp3')
    >>> request.get(link[0])
    '''
    quality_list=('1','2','3')
    quality='3' if quality not in quality_list else quality
    mime_type='mp3' if mime_type not in ('mp3','opus') else mime_type
   
    mime_type = 'opus' if mime_type == 'mp3' and mime_type not in dict1['music'] else 'mp3'
    
    # Retrieve the available quality levels and select the appropriate audio quality
    audio_data = dict1['music'].get(mime_type)
    if audio_data:
        quality_levels = sorted(map(int, audio_data.keys()))
        
        if quality == '1':
            return audio_data[str(quality_levels[0])]
        if quality == '2':
            return audio_data[str(quality_levels[len(quality_levels) // 2])]
        if quality == '3':
            return audio_data[str(quality_levels[-1])]
    return None


def getting_video_info_youtube(video:bool)->tuple[dict,str,str,str]|tuple[list,str]|None:
    """
    Fetches information about a video or playlist from YouTube.

    Args:
        - video (bool): If True, fetches information about a single video. If False, fetches information about a playlist.

    Returns:
        - FOR VIDEOS: --->  tuple[dict, str, str, str] or None: \n
            1. dict , video title, artist name, and thumbnail link if fetched successfully.\n
            2. Returns None if there's an error in collecting data.\n
        - FOR PLAYLIST: --->  tuple[list[str], str] or None:\n
            1. A tuple containing a list of video IDs in the playlist and the playlist title.\n
            2. Returns None if there's an error in collecting data.\n
    """
    logo(stop=False,clear=True)
    link=input(colored("('n' for exit )enter the link to download (^-^)* ","yellow"))
    if link =='n':return 'going back'
    youtube_object=YOUTUBE(link)
    
    if video:
        dict1=get_video_info(youtube_onj=youtube_object)
        
        if dict1 is None:
            _=input(colored("there is some error in collecting data may solve in futube update click enter to continue",'red'))
            return None
        
        #print(prininging info regrading video in formated way)
        print(colored('=' * 60, 'cyan') +
              colored('\nVideo found: ', 'blue') +
              youtube_object.YouTube.title() +
              colored('   Length: ', 'blue') +
              sec_to_min_to_hours(youtube_object.YouTube.length_sec()) +
              colored('\n' + '=' * 60, 'cyan'))
        
        # Return video information
        return (dict1,
                youtube_object.YouTube.title(),
                youtube_object.YouTube.artist_name(),
                youtube_object.YouTube.thumbnail(5))
    else:
        get_all_video_id=youtube_object.playlist.extract_video_id()
        
        if get_all_video_id is None:
            _=input(colored("there is some error while facturing data try after sometime:)",'red'))
            return None
        
        print(colored('='*60,'cyan')+
              colored('\nplaylist name:- ','blue')+
              (youtube_object.playlist.get_title_of_playlist())+
              colored('   total_videos  ','blue')+
              youtube_object.playlist.get_size_of_playlist()+
              colored('\n'+'='*60,'cyan'))
        print(colored('selecting lower resualtion may couse error :)','red'))
        
        return (
            get_all_video_id,
            youtube_object.playlist.get_title_of_playlist())


def audio_downloader_youtube(link_of_music:str, path_to_save:str, ffmpeg_path:str, title_video:str , artist_name:str , thumbnail_link:str)->None:
    """
    Downloads audio from a YouTube link and saves it to the specified path.
    
    Args:
        link_of_music (str): The YouTube link of the music video.
        path_to_save (str): The path where the audio file will be saved.
        ffmpeg_path (str): The path to the FFmpeg executable.
        title_video (str): The title of the video.
        artist_name (str): The name of the artist.
        thumbnail_link (str): The link to the thumbnail image.
        
    Returns:
        None
    """
    # Download audio file to a temporary location
    with NamedTemporaryFile(delete=False , dir=default_path) as temp_audi_path:
        response=download_file_with_resume(link_of_music,temp_audi_path.name)
    
    # Check if the download was successful
    if response:
        # Add cover art and metadata to the audio file
        print(colored('finishing up....wait a...bit adding cover_image...','blue'))
        _add_cover_and_meta_data(temp_audi_path.name,path_to_save,ffmpeg_path,_valid_name(title_video),artist_name,thumbnail_link)
        print(colored('file saved in path :- '+str(path_to_save),'yellow'))
    else:
        # Print error message if download failed
        print(colored('there is some error while dwonloading the file try diffrent resulation :)','red'))
        
    #at last unlink the tenmpfile
    os.unlink(temp_audi_path.name)
    
def video_downloader_youtube(video_staus_if_audio:bool,link_video:str,dict1:dict,attempt_to_download:int,output_path:str,ffmpeg_path:str)->bool:
    '''
    Downloads video from a YouTube link.

    Args:
        video_status_if_audio (bool): Indicates whether the video has audio available.
        link_video (str): The URL of the video to download.
        dict1 (dict): A dictionary containing video information.
        attempt_to_download (int): Number of attempts to download the video.
        output_path (str): The path where the downloaded video will be saved.
        ffmpeg_path (str): The path to the ffmpeg executable.

    Returns:
        bool: True if download is successful, False otherwise.
    '''

    print(colored('video downloading started :)..','blue'))
    # If video has no audio
    if not video_staus_if_audio:
        # Download video
        with NamedTemporaryFile(delete=False,dir=default_path) as video_file:
            response=download_file_with_resume(link_video,video_file.name)
        if not response:return False # if donloading failed then return False
        
        # Start downloading audio
        print(colored('music downloading started :)..','blue'))
        with NamedTemporaryFile(delete=False,dir=default_path) as audio_file:
            music=handeking_error_while_downloading_music(dict1,'3','mp3',audio_file.name,attempt_to_download)
        
        # Add audio to the video if music True then print(error message)
        if music:
            add_audio_to_video(video_file.name,audio_file.name,ffmpeg_path,output_path)
        else:
            print(colored("Failed to add audio in the video :( ","red"))
        #unlinking temp files
        os.unlink(audio_file.name)
        os.unlink(video_file.name)
     # If video has audio
    else:
        # Download the video
        response=download_file_with_resume(link_video,output_path)
        if not response:# Handle download failure
            os.unlink(output_path)
            return False
    return True #returning true becouse every step was sucsessfull



def youtube_dowloader():
    def youtube_audio_downloader():
        """
        Downloads audio from a video, providing options for different resolutions.
        
        Retrieves video information, including available audio formats, from a source.
        Presents the user with options for downloading different resolutions of the audio.
        
        Returns:
            None 'going back'
        """
        #collecting video_info_by the function getting_video_info_youtube
        data=getting_video_info_youtube(video=True)
        if data=='going back':return None
        dict1,title_video,artist_name,thumbnail_link=data
        
        useful_data=[]
        for num,data in enumerate(dict1['music']['mp3'].items(),start=1):
            print(colored('{:<{}}{:<{}}{}'.format(f'[ {str(num)} ]',7,data[1][1],24,get_size(data[0])),'blue'));useful_data.append(data[1][0])
        for num,data in enumerate(dict1['music']['opus'].items(),start=num+1):
            print(colored('{:<{}}{:<{}}{}'.format(f'[ {str(num)} ]',7,data[1][1],24,get_size(data[0])),'blue'));useful_data.append(data[1][0])
        
        path=valid_path_name(default_path,title_video+'.mp3')
        # checking if resulation entered is valid or in range or not if in range or valid pass
        # else print the error message and takes input again till not get valid input
        while not (resulation:=input(colored('enter which resulation video you wanna download?','yellow'))).isdigit() or not 1<=int(resulation)<=num:
            print(colored('please type within in givin option :)','red'))
        
        # downloading audio
        audio_downloader_youtube(useful_data[int(resulation)-1],path,ffmpeg_path,title_video,artist_name,thumbnail_link) 
        
    def video_downloadedr():
        '''
        This function facilitates downloading videos from YouTube.

        It retrieves video information from YouTube and provides options to download the video 
        in different resolutions. If available, it also provides options with and without audio.

        Args:
            None

        Returns:
            None
        '''
        data=getting_video_info_youtube(video=True)
        if data=='going back':return None
        dict1, video_title, artist,thumbnail_link=data
        useful_data=[]
        
        print(colored('best link to download(mp4) - audio avialabe'+'='*30,'yellow'))
        for num,items in enumerate(dict1['video']['audio_aviable'].items(),start=1):print(colored('{:<{}}{:<{}}{}'.format(f'[ {num} ]',7,items[0],13,get_size(items[1][1])),'blue'));useful_data.append([items[1][0],'.mp4',True])
        print(colored('other link to download(mp4) - audio not avialabe'+'='*30,'yellow'))
        for num,items in enumerate(dict1['video']['mp4'].items(),start=num+1):print(colored('{:<{}}{:<{}}{}'.format(f'[ {num} ]',7,items[0],13,get_size(items[1][1])),'blue'));useful_data.append([items[1][0],'.mp4',False])
        print(colored('other link to download(webm) - audio not avialabe'+'='*30,'yellow'))
        for num,items in enumerate(dict1['video']['webm'].items(),start=num+1):print(colored('{:<{}}{:<{}}{}'.format(f'[ {num} ]',7,items[0],13,get_size(items[1][1])),'blue'));useful_data.append([items[1][0],'.webm',False])
        print(colored('video does not have audio don\'t worry we try to add audio :)','yellow'))
        
        while not (resulation:=input(colored('enter which resulation video you wanna download?','yellow'))).isdigit() or not 1<=int(resulation)<=num:
            print(colored('please type within in givin option :)','red'))
            
        path=valid_path_name(default_path,video_title+useful_data[int(resulation)-1][1])
        
        response=video_downloader_youtube(useful_data[int(resulation)-1][2],useful_data[int(resulation)-1][0],dict1,2,path,ffmpeg_path)
        if response :
            print(colored("downloading_commpleted file saved in path:0 "+str(path),'yellow'))
        else:
            print(colored("there is some error - try dwonloading with differnt resulation :(","red"))
        
        
    def playlist_video_downloader():
        '''
        Downloads videos from a YouTube playlist.

        It retrieves all video IDs and titles from a YouTube playlist and provides an option to download videos in a specified resolution.
        
        Args:
            None

        Returns:
            None
        '''
        data=getting_video_info_youtube(video=False)
        if data=='going back':return None
        get_all_video_id,title_playlist=data
        
        while not (resulation:=input(colored('enter resulation [144p,240p,*360p*,480p,*720p*,1080p,1440p,2160p] for downlaoding -> ','blue'))) in ('144p','240p','360p','480p','720p','1080p','1440p','2160p'):
            print(colored('wrong input plese select resulation in the given list','red'))
        
        playlist_saving_dir=valid_dir_name(default_path,title_playlist)
        os.mkdir(playlist_saving_dir)
        
        for num,id in enumerate(get_all_video_id,start=1):
            link=f'https://www.youtube.com/watch?v={id}'
            
            new_youtube_obj=YOUTUBE(link)
            dict1=get_video_info(new_youtube_obj)
            print(colored("="*80,"yellow"))
            
            if dict1 is None:
                print(colored(f'[ {num} ] there is some error while dwonloading the file try diffrent resulation :(','red'))
                print(colored(f"title: {new_youtube_obj.YouTube.title()}\nlink: {link}",'blue'))
                continue
            
            output_path=valid_path_name(playlist_saving_dir,new_youtube_obj.YouTube.title()+'.mp4')
            data_got=get_video_link_by_resulation(dict1,resulation,'mp4')
            
            print(colored(f"[ {num} ] downloading:- {new_youtube_obj.YouTube.title()} size:- {get_size(data_got[0][1])} resulation downlaoding:- {data_got[2]}","blue"))
            response=video_downloader_youtube(data_got[1],data_got[0][0],dict1,2,output_path,ffmpeg_path)
            
            if response :
                print(colored("downloading_commpleted file saved in path:0 "+str(output_path),'yellow'))
            else:
                print(colored("there is some error - try dwonloading with differnt resulation :(","red"))
            
    def playlist_audio_downloaderr():
        """
        Downloads audio files from YouTube playlist.

        Fetches information about videos in a YouTube playlist and downloads their audio.
        The user is prompted to select the quality of the audio to download.

        Returns:
            None
        """
        # Get playlist information
        data=getting_video_info_youtube(video=False)
        if data=='going back':return None
        get_all_video_id,title_playlist=data
        
        # Prompt user to select audio quality
        while not (quality:=input(colored('enter quality (lower[1] medium[2] higher[3] ) for downlaoding -> [1/2/3]','blue'))) in ('1','2','3'):
            print(colored('wrong input plese select resulation in the given list','red'))
            
        # Create directory to save playlist audio files
        playlist_saving_dir=valid_dir_name(default_path,title_playlist)
        os.mkdir(playlist_saving_dir)
        
        # Download audio for each video in the playlist
        for num,id in enumerate(get_all_video_id,start=1):
            link=f'https://www.youtube.com/watch?v={id}'
            
            new_youtube_obj=YOUTUBE(link)
            dict1=get_video_info(new_youtube_obj)
            print(colored("="*80,"yellow"))
            
            if dict1 is None:# if dict1 is None then go directally for next audio to download
                print(colored(f'[ {num} ] there is some error while dwonloading the file try diffrent resulation :(','red')),
                print(colored(f"title: {new_youtube_obj.YouTube.title()}\nlink: {link}",'blue'))
                continue
            
            output_path=valid_path_name(playlist_saving_dir,new_youtube_obj.YouTube.title()+'.mp3')
            link=get_audio_link_quality(dict1,quality,'mp3')[0]
            
            print(colored(f"[ {num} ] downloadiing:- {new_youtube_obj.YouTube.title()}","blue")),
            audio_downloader_youtube(link,output_path,ffmpeg_path,new_youtube_obj.YouTube.title(),new_youtube_obj.YouTube.artist_name(),new_youtube_obj.YouTube.thumbnail(5))

    while True:
        logo(stop=False,clear=True)
        print(colored("what u wanna download in youtube?","yellow"))
        print(colored("[ 1 ] video downloader \n"
              +"[ 2 ] audio downloader \n"
              +"[ 3 ] playlist video downloader \n"
              +"[ 4 ] playlist audio downloader \n"
              +"[ 5 ] Go back",'cyan'))
        response=input(colored("tour response here:) ",'red'))
        match response:
            case '1':video_downloadedr()
            case '2':youtube_audio_downloader()
            case '3':playlist_video_downloader()
            case '4':playlist_audio_downloaderr()
            case '5':break
            case _:_=input(colored('you typed somthing wrong :) tap enter to continue','red'))
        _=input(colored('tap enter to continue :).. ','blue'))
def facebook_downloader():pass
def instagrama_downloader():pass
def pinterest_downloader():pass
def whatsapp_downloader():pass
def spotiy_downloader():pass
def other_downloader():pass
def setting():pass
def main():
    while True:
        logo(stop=True,clear=True)
        print(colored('what u wanna download here :)\n','yellow')
            +colored("="*40,'black')+'\n'
            +colored("[ 1 ] YouTube Downloader\n",'red')
            +colored("[ 2 ] FaceBook Downloader\n",'blue')
            +colored("[ 3 ] InstaGram Downloader\n",'magenta')
            +colored("[ 4 ] Pinterest Downloader\n",'light_red')
            +colored("[ 5 ] Whatsapp status Downloader\n",'green')
            +colored("[ 6 ] Spotfy audio downloader \n",'light_green')
            +colored("[ 7 ] others downloader....\n",'cyan')
            +colored("[ 8 ] settings \n",'cyan')
            +colored("[ 9 ] quite\n",'cyan')
            +colored("="*40,'black'))
        response=input(colored("your response here ^^ ",'yellow'))
        match response:
            case '1':youtube_dowloader()
            case '2':facebook_downloader()
            case '3':instagrama_downloader()
            case '4':pinterest_downloader()
            case '5':whatsapp_downloader()
            case '6':spotiy_downloader()
            case '7':other_downloader()
            case '8':setting()
            case '9':break
            case _:_=input(colored('u typed something wrong :) type within givin range of option','red'))

if __name__=="__main__":
    #this line becouse some terminal don't show color at first till we don't use os.system('cls)
    print(colored('made by akki free to use :) ','yellow'))
    os.system('cls')
    main()
    #message for devs------->:)
    
    # well if u ask me  why i am downloading everything manually by collecting 
    # streaming data so simple answeer i was going to use pytube download moduel 
    # but i try to get progress bar and that was'nt worked like it's downloading 
    # but not showing progress i tried mnay ways bt not worked so i just used it 
    # i made whole thing to download youtube video just using pytube streaming 
    # moduel to get the data :) in future i won't use that too well i mean i try 
    # not to use :) will try to find a way if u have any tell me:)
