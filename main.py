import subprocess

streamlit_command = "streamlit run MainPage.py"

subprocess.run(streamlit_command, shell=True, cwd="Streamlit")