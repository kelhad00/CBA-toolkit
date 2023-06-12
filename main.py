import subprocess

def install_missing_modules():
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
    print("Terminé !")

streamlit_command = "streamlit run MainPage.py"

install_missing_modules()
subprocess.run(streamlit_command, shell=True, cwd="Streamlit")