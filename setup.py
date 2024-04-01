import subprocess
import os
from main import colored

def steps_7z(path):
    print(colored("7z is not in system variable path please follow the steps:- ", "red"))
    print(colored(f"Step 1: Please go to the path {path} and extract 'ffmpeg.7z' file", "blue"))
    print(colored("After extracting the folder, without modifying anything in that folder,", "blue"))
    print(colored(f"paste it on the same path: {path}", "blue"))
    print(colored("Then run main.py to see if everything is okay or not", "yellow"))

def ownffmpeg():
    print(colored("If you have your own ffmpeg, please set up the ffmpeg path in the main.py. Here are the steps:", "yellow"))
    print(colored("Step 1: Go to main.py, run it, click enter, then press 8 and enter to go to settings", "blue"))
    print(colored("Step 2: Type 'edit' and enter", "blue"))
    print(colored("Step 3: Press 2 to edit ffmpeg path, then add the path and click enter. Go back to the main menu.", "blue"))
    print(colored("Now you can use PyStreamSaver to save any stream from any website. Thank you.", "blue"))
    print(colored("Author: Akki", "blue"))

def extract_7z(file_path):
    try:
        # Get the directory containing the 7z file
        output_dir = os.path.dirname(file_path)
        
        # Construct the command to extract the 7z file using the 7z command-line utility
        command = ['7z', 'x', file_path, f'-o{output_dir}']

        # Execute the command
        subprocess.run(command, check=True)
        
        print(f"Successfully extracted {file_path} to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to extract {file_path}. Return code: {e.returncode}")
        ownffmpeg()

print("This setup.py is just an initial setup.py. When this project is completed, it will be improved.\n")

print(colored('PyStreamSaver code author: Akhand Raj (akki_raj)', "yellow"))
print(colored('Instagram: @its_just_me_akki', "blue"))
print(colored('Personal Instagram: @akki_raj_._\n', "blue"))

print(colored('Setting up ffmpeg', "yellow"))
path = '.\\PyStreamSaver_data\\ffmpeg.7z'
try:
    extract_7z(path)
except FileNotFoundError:
    steps_7z(path)
    ownffmpeg()
