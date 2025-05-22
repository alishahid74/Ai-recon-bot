# AI Recon Bot - v0.5 with .env API Key Support

import subprocess
import json
import re
import os
from urllib.parse import urlparse
from openai import OpenAI
from dotenv import load_dotenv

print(r"""
   █████╗ ██╗██████╗ ███████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗
  ██╔══██╗██║██╔══██╗██╔════╝██╔════╝ ██╔══██╗██╔═══██╗████╗  ██║
  ███████║██║██████╔╝█████╗  ██║  ███╗██████╔╝██║   ██║██╔██╗ ██║
  ██╔══██║██║██╔═══╝ ██╔══╝  ██║   ██║██╔═══╝ ██║   ██║██║╚██╗██║
  ██║  ██║██║██║     ███████╗╚██████╔╝██║     ╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═══╝

              AI Recon Bot  •  Hunt Smarter, Not Harder 🕵️‍♂️
""")



# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_subdomains(domain):
    try:
        result = subprocess.run(["subfinder", "-d", domain, "-silent"], capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running subfinder: {e}")
        return []

def get_endpoints(domain):
    cache_file = f"cache_gau_{domain}.txt"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return f.read().splitlines()

    try:
        result = subprocess.run(["gau", domain], capture_output=True, text=True, check=True, timeout=30)
        urls = list(set(result.stdout.splitlines()))
        with open(cache_file, "w") as f:
            f.write("\n".join(urls))
        return urls
    except subprocess.TimeoutExpired:
        print(f"[!] gau timed out on {domain}, skipping.")
        return []
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running gau: {e}")
        return []

# Parameter and endpoint classification
def extract_parameters(endpoints):
    param_pattern = re.compile(r'[?&](\w+)=')
    params = {}
    for url in endpoints:
        matches = param_pattern.findall(url)
        for param in matches:
            if param not in params:
                params[param] = []
            params[param].append(url)
    return params

def classify_endpoint(url):
    classifications = {
        'auth': ['login', 'logout', 'signin', 'signup'],
        'admin': ['admin', 'dashboard', 'backend'],
        'uploads': ['upload', 'file', 'media'],
        'api': ['api', 'v1', 'v2']
    }
    parsed = urlparse(url)
    path = parsed.path.lower()
    for category, keywords in classifications.items():
        if any(keyword in path for keyword in keywords):
            return category
    return 'other'

def classify_all(endpoints):
    classification = {}
    for url in endpoints:
        cat = classify_endpoint(url)
        if cat not in classification:
            classification[cat] = []
        classification[cat].append(url)
    return classification

# AI-enhanced endpoint analysis
def ai_classify_endpoint(endpoint):
    prompt = f"""Classify this web endpoint based on its URL structure: {endpoint}.
Possible categories: authentication, administration, API, file upload, user interaction, unknown."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cybersecurity assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"[!] OpenAI API error: {e}")
        return "unknown"

def ai_classify_all(endpoints):
    classified = {}
    for url in endpoints:
        category = ai_classify_endpoint(url)
        if category not in classified:
            classified[category] = []
        classified[category].append(url)
    return classified

# Entry point
def recon(domain):
    print(f"[+] Gathering subdomains for: {domain}")
    subdomains = get_subdomains(domain)

    print(f"[+] Gathering endpoints using gau")
    endpoints = []
    limited_subdomains = subdomains[:10]  # Limit for speed and stability
    for i, sub in enumerate(limited_subdomains, 1):
        print(f"[{i}/{len(limited_subdomains)}] Running gau on {sub}")
        endpoints.extend(get_endpoints(sub))

    print(f"[+] Extracting parameters")
    parameters = extract_parameters(endpoints)

    print(f"[+] Classifying endpoints using basic logic")
    grouped = classify_all(endpoints)

    print(f"[+] Enhancing classification using AI")
    ai_grouped = ai_classify_all(endpoints[:20])  # Limit for demo

    output = {
        'subdomains': subdomains,
        'parameters': parameters,
        'basic_classified_endpoints': grouped,
        'ai_classified_endpoints': ai_grouped
    }
    return output

if __name__ == "__main__":
    domain = input("Enter target domain: ")
    results = recon(domain)
    with open("ai_recon_output.json", "w") as f:
        json.dump(results, f, indent=2)
    print("[+] Recon complete. Results saved to ai_recon_output.json")

