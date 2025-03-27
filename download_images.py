import os
import requests
from urllib.parse import urlparse

def download_file(url, local_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {local_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Create necessary directories
os.makedirs("img/profile", exist_ok=True)
os.makedirs("img/projects", exist_ok=True)
os.makedirs("img/skills", exist_ok=True)

# Dictionary of images to download
images = {
    # Skills icons
    "img/skills/vscode.svg": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg",
    "img/skills/jupyter.svg": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg",
    "img/skills/excel.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg/240px-Microsoft_Office_Excel_%282019%E2%80%93present%29.svg.png",
    "img/skills/colab.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Google_Colaboratory_SVG_Logo.svg/240px-Google_Colaboratory_SVG_Logo.svg.png",
    "img/skills/powerbi.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/New_Power_BI_Logo.svg/240px-New_Power_BI_Logo.svg.png",
    "img/skills/chatgpt.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/240px-ChatGPT_logo.svg.png",
    "img/skills/claude.ico": "https://claude.ai/favicon.ico",
    
    # Project images (using placeholder images for now)
    "img/projects/portfolio.jpg": "https://placehold.co/800x600/4169E1/ffffff?text=Portfolio+Website",
    "img/projects/task-manager.jpg": "https://placehold.co/800x600/4169E1/ffffff?text=Task+Manager+App",
    "img/projects/weather-app.jpg": "https://placehold.co/800x600/4169E1/ffffff?text=Weather+Dashboard",
    "img/projects/ecommerce.jpg": "https://placehold.co/800x600/4169E1/ffffff?text=E-commerce+Platform"
}

# Download each image
for local_path, url in images.items():
    download_file(url, local_path)

print("\nImage download complete! Please add your profile picture manually to:")
print("- img/profile/Pratu.jpeg") 