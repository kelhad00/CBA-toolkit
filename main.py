import subprocess

# Commande à exécuter dans le terminal du dossier Streamlit
streamlit_command = "Streamlit run MainPage.py"

# Exécuter la commande dans le terminal
subprocess.run(streamlit_command, shell=True, cwd="Streamlit")