# AI Recon Bot 🔍🤖

A smart subdomain and endpoint recon tool powered by AI classification. Built for bug bounty hunters, penetration testers, and ethical hackers who want more context-aware reconnaissance.

## ✨ Features

* Subdomain enumeration using `subfinder`
* Historical endpoint discovery using `gau`
* Parameter and endpoint classification
* AI-powered endpoint type prediction (auth, admin, uploaders, APIs)
* Caching + timeout handling
* `.env` support for API key management

## 📦 Installation

### On Kali Linux

```bash
git clone https://github.com/YOUR_USERNAME/ai-recon-bot.git
cd ai-recon-bot
bash install_ai_recon.sh
```

## 🔐 Configuration

Create a `.env` file in the same directory:

```
OPENAI_API_KEY=sk-your-api-key-here
```

### ⚠️ Important: Provide Your Own API Key

To use the AI-powered classification, you must:

* Have an [OpenAI API key](https://platform.openai.com/account/api-keys)
* Ensure your billing is active and quota is not exceeded

If you encounter this error:

```
[!] OpenAI API error: Error code: 429 - {'error': {'message': 'You exceeded your current quota...'}}
```

It means your account has run out of free credits or paid quota. To fix this:

1. Log into [OpenAI Dashboard](https://platform.openai.com/account/billing)
2. Add a payment method or wait for the next billing cycle
3. Generate a valid API key and update your `.env`

## 🚀 Usage

```bash
source ai_recon_env/bin/activate
python AI_bot.py
```

You will be prompted to enter a target domain.

## 🔧 Requirements

Python 3.8+ and `go` language installed. Also ensures these tools are in your path:

* `subfinder`
* `gau`

## 📊 Output

* `ai_recon_output.json`: Contains subdomains, parameters, basic & AI-classified endpoints.
* `cache_gau_<domain>.txt`: Saved gau results per subdomain to prevent re-querying.




Made with ❤️ by Hak
