from mutagen.id3 import ID3,APIC,TIT2,TPE1,TALB
from PIL import Image
from tempfile import NamedTemporaryFile
from io import BytesIO
import subprocess
import requests
import os
from youtube import YOUTUBE

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!important_variables!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
default_path='C:\\Users\\DELL\\Desktop\\side project'
ffmpeg_path='C:\\ffmpeg\\ffmpeg-2024-03-11-git-3d1860ec8d-full_build\\bin\\ffmpeg.exe'

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
    
    
def colored(string,color)->str:
    """
    Return the input string with specified color in ANSI escape sequence.

    Parameters:
    - string (str): The input string to be colored.
    - color (str): The color name. Supported color names are 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white', and 'reset'.

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
        'reset': '\x1b[0m'
    }
    # Color escape sequences are added before the string and default to white color at the end (\x1b[0m).
    color_code=colors.get(color.lower(),'\x1b[0m')
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
    bar = colored('[','yellow') + colored('=','blue') * blocks_compleated-1+colored('>','yellow') + ' ' * (length - blocks_compleated) + colored(']','yellow')
    percentage = colored('{:.0%}'.format(progress),'blue')
    print('\r' + bar + ' ' + percentage, end='', flush=True)


def valid_name(name:str)->str:
    '''this function takes string as an argument and return string that is valid for making file and dir in the window'''
    return ''.join(a if not a in '<>:"/\\|?*' else '_' for a in name)



def valid_path_name(dir_path,name:str)->str:
    '''This func return valid name for maiking file in window if name already exists modify the name and return it\n
    takes dir path and name of file +.extention of file as argument'''
    name,extention=valid_name(name).rsplit('.', 1)
    number=1
    extra=''
    while os.path.exists(dir_path+'\\'+name+extra+'.'+extention):
        extra=f'({number})'
        number+=1
    return dir_path+'\\'+name+extra+'.'+extention

def valid_dir_name(dir_path:str,name:str)->str:
    '''this function return valid name for making dir in window if name already exists modify the name and returun it\n
    takes dir_path and name of dir u wanna make as an argumnet'''
    name=valid_name(name)
    extra=''
    number=1
    while os.path.exists(dir_path+'\\'+name+extra):
        extra=f'({number})'
        number+=1
    return dir_path+'\\'+name+extra

def crop_center_square(image_path)->bytes:
    """
    Crop the image to center it on a 1:1 aspect ratio.

    Parameters:
    - image_path (str): The path to the image file.

    Returns:
    - bytes: The cropped image data in bytes format.

    Example:
    >>> cropped_image_bytes = crop_center_square("image.jpg")

    Note:
    - This function crops the image to make it a square by taking the larger dimension (width or height) and
      cropping from the center to achieve a 1:1 aspect ratio.
    - The input image should be in JPEG format.
    
    -writen by chat gpt 3.5 
    """
    with open(image_path,'rb')as f:
        image_data=f.read()
    img = Image.open(BytesIO(image_data))
    width, height = img.size
    output_buffer = BytesIO()
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    img = img.crop((left, top, right, bottom))
    img.save(output_buffer, format='JPEG')
    image_bytes = output_buffer.getvalue()
    return image_bytes
    
    
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
    
    
def add_cover_in_music(audio_file_path, title, artist, cover_photo_url,):
    '''this will add image in audio file and more meta info like title artist and album'''
    response = requests.get(cover_photo_url)
    if response.status_code==200:
        audio_tags = ID3()
        audio_tags.add(TIT2(encoding=3, text=title))
        audio_tags.add(TPE1(encoding=3, text=artist))
        audio_tags.add(TALB(encoding=3, text=artist))
        with NamedTemporaryFile(delete=False) as temp_file:temp_file.write(response.content)
        cropped_img = crop_center_square(temp_file.name)
        if cropped_img.startswith(b'\xff\xd8\xff'):cover_mime='image/jpeg'
        elif cropped_img.startswith(b'\x89PNG\r\n\x1a\n'):cover_mime='image/png'
        apic = APIC(encoding=3, mime=cover_mime, type=3, desc=u'Cover', data=cropped_img)
        audio_tags.add(apic)
        audio_tags.save(audio_file_path)
        os.unlink(temp_file.name)
    else:print(colored('failed to add cover art ','red'))
    

def download_file_with_resume(url, filename, retry=1):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    downloaded_bytes=0
    headers = {'Range': f'bytes={downloaded_bytes}-'}
    response = requests.get(url, headers=headers, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    custom_progress_bar(downloaded_bytes, total_size)
    try:
        with open(filename, 'ab') as f:
            for chunk in response.iter_content(chunk_size=4096):
                if not chunk: continue
                f.write(chunk)
                downloaded_bytes += len(chunk)
                custom_progress_bar(downloaded_bytes, total_size)
        print()
        return True
    except Exception:return None


def handeking_error_while_downloading_music(dict1,quality:str,mime_type,output_path,attempt_to_download=1):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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


def youtube_dowloader():
    def audio_downloader():
        logo(stop=False,clear=True)
        link=input(colored("enter the downlaod link(^-^) ","yellow"))
        youtube_object=YOUTUBE(link)
        
        #getting _info_by_sourse
        dict1=get_video_info(youtube_onj=youtube_object)
        if dict1 is None:_=input(colored("there is some error in collecting data may solve in futube update click enter to continue",'red'));return None
        print(colored('='*60,'cyan')+colored('\nvideo found name:- ','blue')+(title_video:=youtube_object.YouTube.title())+colored('   lenth:- :','blue')+sec_to_min_to_hours(youtube_object.YouTube.lenth_sec())+colored('\n'+'='*60,'cyan'))
        useful_data=[]
        
        for num,data in enumerate(dict1['music']['mp3'].items(),start=1):
            print(colored('{:<{}}{:<{}}{}'.format(f'[ {str(num)} ]',7,data[1][1],24,get_size(data[0])),'blue'));useful_data.append(data[1][0])
        for num,data in enumerate(dict1['music']['opus'].items(),start=num+1):
            print(colored('{:<{}}{:<{}}{}'.format(f'[ {str(num)} ]',7,data[1][1],24,get_size(data[0])),'blue'));useful_data.append(data[1][0])
        path=valid_path_name(default_path,title_video+'.mp3')
        while not (resulation:=input(colored('enter which resulation video you wanna download?','yellow'))).isdigit() or not 1<=int(resulation)<=num:print(colored('please type within in givin option :)','red'))

        with NamedTemporaryFile(delete=False,dir=default_path)as temp_audi_path:
            response=download_file_with_resume(useful_data[int(resulation)-1],temp_audi_path.name)
        if response:
            print(colored('finishing up....wait a...bit adding cover_image...','blue'))
            convert_audio(temp_audi_path.name,path,ffmpeg_path)
            add_cover_in_music(path,valid_name(title_video),youtube_object.YouTube.artist_name(),youtube_object.YouTube.thumbnail(5))
            os.unlink(temp_audi_path.name)
            print(colored('file saved in path :- '+str(path),'yellow'))
        else:
            os.unlink(temp_audi_path.name)
            print(colored('there is some error while dwonloading the file try diffrent resulation :)','red'))

    def video_downloadedr():
        logo(stop=False,clear=True)
        link=input(colored("enter the downlaod link(^-^) ","yellow"))
        youtube_object=YOUTUBE(link)
        dict1=get_video_info(youtube_object)
        if dict1 is None:_=input(colored("there is some error in collecting data may solve in futube update click enter to continue",'red'));return None
        print(colored('='*60,'cyan')+colored('\nvideo found name:- ','blue')+(title_video:=youtube_object.YouTube.title())+colored('   lenth:- :','blue')+sec_to_min_to_hours(youtube_object.YouTube.lenth_sec())+colored('\n'+'='*60,'cyan'))
        if dict1 is None:_=input(colored("there is some error in collecting data may solve in futube update click enter to continue",'red'));return None
        useful_data=[]
        
        print(colored('best link to download(mp4) - audio avialabe'+'='*30,'yellow'))
        for num,items in enumerate(dict1['video']['audio_aviable'].items(),start=1):print(colored('{:<{}}{:<{}}{}'.format(f'[ {num} ]',7,items[0],13,get_size(items[1][1])),'blue'));useful_data.append([items[1][0],'.mp4',True])
        print(colored('other link to download(mp4) - audio not avialabe'+'='*30,'yellow'))
        for num,items in enumerate(dict1['video']['mp4'].items(),start=num+1):print(colored('{:<{}}{:<{}}{}'.format(f'[ {num} ]',7,items[0],13,get_size(items[1][1])),'blue'));useful_data.append([items[1][0],'.mp4',False])
        print(colored('other link to download(webm) - audio not avialabe'+'='*30,'yellow'))
        for num,items in enumerate(dict1['video']['webm'].items(),start=num+1):print(colored('{:<{}}{:<{}}{}'.format(f'[ {num} ]',7,items[0],13,get_size(items[1][1])),'blue'));useful_data.append([items[1][0],'.webm',False])
        print(colored('video does not have audio don\'t worry we try to add audio :)','yellow'))
        
        while not (resulation:=input(colored('enter which resulation video you wanna download?','yellow'))).isdigit() or not 1<=int(resulation)<=num:print(colored('please type within in givin option :)','red'))
        path=valid_path_name(default_path,title_video+useful_data[int(resulation)-1][1])
        
        if not useful_data[int(resulation)-1][2]:
            print(colored('video downloading started :)..','blue'))
            with NamedTemporaryFile(delete=False,dir=default_path) as video_file:
                response=download_file_with_resume(useful_data[int(resulation)-1][0],video_file.name)
            if response:pass
            else:
                _=input(colored('failed to download the video please try again with differnt resultion "tap enter to continue"','red'))
                os.unlink(video_file.name);return None
            print(colored('music downloading started :)..','blue'))
            with NamedTemporaryFile(delete=False,dir=default_path) as audio_file:
                response=handeking_error_while_downloading_music(dict1,'3','mp3',audio_file.name,attempt_to_download=2)
            if response:pass
            else:
                _=input(colored('failed to download the music please try again with differnt resultion "tap enter to continue"','red'))
                os.unlink(audio_file.name);os.unlink(video_file.name);return None
                
            add_audio_to_video(video_file.name,audio_file.name,ffmpeg_path,path)
            os.unlink(audio_file.name)
            os.unlink(video_file.name)
            print(colored('file saved in path :- '+str(path),'yellow'))
        else:
            print(colored('video downloaded started :)..','blue'))
            response=download_file_with_resume(useful_data[int(resulation)-1][0],path)
            if not response:
                os.unlink(path)
                print(colored("there is some error - try dwonloading with differnt resulation :("))
            else:
                print(colored("downloading_commpleted file saved in path:0 "+str(path),'yellow'))

    def playlist_video_downloader():
        logo(stop=False,clear=True)
        link=input(colored("enter the playlist link(^-^) ","yellow"))
        playlist=YOUTUBE(link)
        
        get_all_video_id=playlist.playlist.extract_video_id()
        if get_all_video_id is None:_=input(colored("there is some error while facturing data try after sometime:)",'red'));return None
        print(colored('='*60,'cyan')+colored('\nplaylist name:- ','blue')+(title_playlist:=playlist.playlist.get_title_of_playlist())+colored('   total_videos  ','blue')+playlist.playlist.get_size_of_playlist()+colored('\n'+'='*60,'cyan'))
        print(colored('selcting low resulation like 144p and 240p may couse error :)','red'))
        while not (resulation:=input(colored('enter resulation [144p,240p,*360p*,480p,*720p*,1080p,1440p,2160p] for downlaoding -> ','blue'))) in ('144p','240p','360p','480p','720p','1080p','1440p','2160p'):print(colored('wrong input plese select resulation in the given list','red'))
        
        playlist_saving_dir=valid_dir_name(default_path,title_playlist)
        os.mkdir(playlist_saving_dir)
        
        for num,id in enumerate(get_all_video_id,start=1):
            link=f'https://www.youtube.com/watch?v={id}'
            new_youtube_obj=YOUTUBE(link)
            dict1=get_video_info(new_youtube_obj)
            if dict1 is None:
                print(colored("="*80,"yellow")+'\n'+colored(f'[ {num} ] there is some error while dwonloading the file try diffrent resulation :(','red'))
                print(colored(f"title: {new_youtube_obj.YouTube.title()}\nlink: {link}",'blue')+'\n'+colored("="*80,"yellow"))
                continue
            data_got=get_video_link_by_resulation(dict1,resulation,'mp4')
            if data_got is None:_=input(colored("there is some errro please try another time "));return None
            link=data_got[0][0]
            print(colored("="*80,"yellow")+'\n'+colored(f"[ {num} ] downloadiing:- {new_youtube_obj.YouTube.title()} size:- {get_size(data_got[0][1])} resulation downlaoding:- {data_got[2]}","blue")+'\n'+colored("="*80,"yellow"))
            output_path=valid_path_name(playlist_saving_dir,new_youtube_obj.YouTube.title()+'.mp4')
            if not data_got[1]:
                print(colored('video downloading started :)..','blue'))
                with NamedTemporaryFile(delete=False,dir=default_path) as video_file:
                    response=download_file_with_resume(link,video_file.name)
                if response:pass
                else:
                    _=input(colored('failed to download the video please try again with differnt resultion "tap enter to continue"','red'))
                    os.unlink(video_file.name);return None
                print(colored('music downloading started :)..','blue'))
                with NamedTemporaryFile(delete=False,dir=default_path) as audio_file:
                    response=handeking_error_while_downloading_music(dict1,'3','mp3',audio_file.name,attempt_to_download=2)
                if response:pass
                else:
                    _=input(colored('failed to download the music please try again with differnt resultion "tap enter to continue"','red'))
                    os.unlink(audio_file.name);os.unlink(video_file.name);continue
                add_audio_to_video(video_file.name,audio_file.name,ffmpeg_path,output_path)
                os.unlink(audio_file.name)
                os.unlink(video_file.name)
                print(colored('file saved in path :- '+str(output_path),'yellow'))
            else:
                print(colored('video downloaded started :)..','blue'))
                response=download_file_with_resume(link,output_path)
                if not response:
                    os.unlink(output_path)
                    print(colored("there is some error - try dwonloading with differnt resulation :("))
                else:
                    print(colored("downloading_commpleted file saved in path:0 "+str(output_path),'yellow'))
            print(colored("="*80,"yellow"))
            

    def playlist_audio_downloaderr():
        logo(stop=False,clear=True)
        link=input(colored("enter the playlist link(^-^) ","yellow"))
        playlist=YOUTUBE(link)
        
        get_all_video_id=playlist.playlist.extract_video_id()
        if get_all_video_id is None:_=input(colored("there is some error while facturing data try after sometime:)",'red'));return None
        print(colored('='*60,'cyan')+colored('\nplaylist name:- ','blue')+(title_playlist:=playlist.playlist.get_title_of_playlist())+colored('   total_videos  ','blue')+playlist.playlist.get_size_of_playlist()+colored('\n'+'='*60,'cyan'))
        print(colored('selecting lower resualtion may couse error :)','red'))
        while not (quality:=input(colored('enter quality (lower[1] medium[2] higher[3] ) for downlaoding -> [1/2/3]','blue'))) in ('1','2','3'):print(colored('wrong input plese select resulation in the given list','red'))
        
        playlist_saving_dir=valid_dir_name(default_path,title_playlist)
        os.mkdir(playlist_saving_dir)
        
        for num,id in enumerate(get_all_video_id,start=1):
            link=f'https://www.youtube.com/watch?v={id}'
            new_youtube_obj=YOUTUBE(link)
            dict1=get_video_info(new_youtube_obj)
            if dict1 is None:
                print(colored("="*80,"yellow")+'\n'+colored(f'[ {num} ] there is some error while dwonloading the file try diffrent resulation :(','red'))
                print(colored(f"title: {new_youtube_obj.YouTube.title()}\nlink: {link}",'blue')+'\n'+colored("="*80,"yellow"))
                continue
            output_path=valid_path_name(playlist_saving_dir,new_youtube_obj.YouTube.title()+'.mp3')
            link=get_audio_link_quality(dict1,quality,'mp3')[0]
            
            print(colored("="*80,"yellow")+'\n'+colored(f"[ {num} ] downloadiing:- {new_youtube_obj.YouTube.title()}","blue"))
            with NamedTemporaryFile(delete=False,dir=default_path)as temp_audi_path:
                response=download_file_with_resume(link,temp_audi_path.name)
            if response:
                print(colored('finishing up....wait a...bit adding cover_image...','blue'))
                convert_audio(temp_audi_path.name,output_path,ffmpeg_path)
                add_cover_in_music(output_path,valid_name(new_youtube_obj.YouTube.title()),new_youtube_obj.YouTube.artist_name(),new_youtube_obj.YouTube.thumbnail(5))
                os.unlink(temp_audi_path.name)
                print(colored('file saved in path :- '+str(output_path),'yellow')+'\n'+colored("="*80,"yellow"))
            else:
                os.unlink(temp_audi_path.name)
                print(colored("="*80,"yellow")+'\n'+colored(f'[ {num} ] there is some error while dwonloading the file try diffrent resulation :)','red')+'\n'+colored("="*80,"yellow"))

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
            case '2':audio_downloader()
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
