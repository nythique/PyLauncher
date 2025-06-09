import os
from dotenv import load_dotenv
load_dotenv()
# NOTE:========================== CONFIGURATION DU MINIMAL ==========================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_TOKEN = os.getenv("GROQ_TOKEN")
VERSION = os.getenv("VERSION")
PREFIX = "-"

# NOTE:========================== IDENTIFIANTS ET CONFIGURATION ==========================
SUPPORT_GUILD_ID = 1328845912117739560
NOTIFS_CHANNEL_ID = 1328845912646356994
REPORT_CHANNEL_ID = 1360403767274508355

# NOTE:========================== CHEMINS DES FICHIERS ========================== 
ERROR_LOG_PATH = r"logs/error/error.log"
SECURITY_LOG_PATH = r"logs/security/security.log"
GLOBAL_DATA_PATH = r"home/cluster/global/firewall.json"
GLOBAL_CHANNEL_PATH = r"home/cluster/global/pipeline.json"
TEMP_UPLOAD_PATH = r"home/cluster/temp" 
CONTROLLER_PATH = r"config/controller/roots.json" 

# NOTE:========================== CONFIGURATION DE L'IA ==========================
MODEL = "llama3-70b-8192" 
FREQUENCY = 1  
TEMPERATURE = 0 
MAX_TOKENS = 256  
TOP_P = 0.95  
PRESENCE_PENALTY = 0  