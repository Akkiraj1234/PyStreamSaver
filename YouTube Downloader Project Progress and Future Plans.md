# YouTube Downloader Project Progress and Future Plans

## 17 march 2024 - 29 march 2024
<!--( checked ) for making it check true -->

**[ Done ]** finish rufe youtube downloader section

**[ Done ]** make sure audio downloader and video downloader working well

**[ Done ]** make sure playlist audio downloader and playlist   video downloader working well

**[ Done ]** then focuse on how i can do all work without using pytube library

**[ Done ]** publish it on git hub

## 29 March 2024 - 01 April 2024

**[ Done ]** rewrite code in a structured and readable way with proper documentation

**[ Done ]** create a comprehensive README file

**[ Done ]** improve all 4 functions in the YouTube downloader library

**[ ===> ]** further improve the YouTube library, fix init function in main YOUTUBE module, and add proper docstrings to all functions

**[ Done ]** avoid using the following libraries:

1. **mutagen:** This module is used for reading and writing audio metadata, including ID3 tags. We will utilize ffmpeg instead.
2. **PIL (Python Imaging Library):** This is now known as Pillow, a Python Imaging Library fork, used for working with images in Python. We can achieve the same functionality with ffmpeg.
3. **termcolor:** Create a function for producing colored terminal text.
4. ~~**subprocess:** This module is used for spawning new processes, connecting to their input/output/error pipes, and obtaining their return codes.~~

## 01 April 2024 - TBD

**[ ------ ]** PIL (Python Imaging Library): *This is now known as Pillow, a Python Imaging Library fork, used for working with images in Python. We will explore alternatives, possibly leveraging ffmpeg.*

**[ ------ ]** start working on the Pinterest download section

## Future

**[ ------ ]** write our own request library

**[ ------ ]** Implement downloading of YouTube 18+ content

**[ ------ ]**  Implement downloading of YouTube restricted videos related to self-harm content

**[ ------ ]**  Implement decrypting YouTube tokenized URLs

**[ ------ ]**  Create a GUI interface using either Tkinter or PyQt
