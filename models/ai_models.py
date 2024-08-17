import requests
import json

# Use Joe's OpenRouter API key
OPENROUTER_API_KEY = "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"
YOUR_SITE_URL = "your-site-url"  # Optional, used for OpenRouter rankings
YOUR_APP_NAME = "YouTube Transcriber AI V1.1"  # Optional, used for OpenRouter rankings

def summarize_with_model(model_name, text):
    prompt = (
        "Please summarize the key points of the following video transcript in a well-structured format, "
        "using bullet points where necessary. Include relevant timings from the video if possible:\n\n{text}"
    )
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": f"{YOUR_SITE_URL}",
            "X-Title": f"{YOUR_APP_NAME}",
        },
        data=json.dumps({
            "model": model_name,
            "messages": [
                {"role": "user", "content": prompt.format(text=text)}
            ]
        })
    )

    try:
        response_data = response.json()
        if "choices" in response_data and response_data["choices"]:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: Unexpected response structure - {response_data}"
    except json.JSONDecodeError:
        return f"Error: Failed to decode JSON response - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_with_gpt4(text):
    return summarize_with_model("gpt-4o-mini", text)

def summarize_with_sonnet(text):
    return summarize_with_model("anthropic/claude-3.5-sonnet", text)

def summarize_with_llama(text):
    return summarize_with_model("meta-llama/llama-3.1-405b-instruct", text)

def get_all_summaries(text):
    return {
        "GPT-4o-Mini": summarize_with_gpt4(text),
        "Sonnet": summarize_with_sonnet(text),
        "Llama": summarize_with_llama(text),
    }
