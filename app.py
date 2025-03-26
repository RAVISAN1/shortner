from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os

app = Flask(__name__)

def bypass_shortner_in_headless(url):
    try:
        
        options = Options()
        options.headless = True
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        
        driver = webdriver.Chrome(options=options)
        
        
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        driver.get(url)
        
        )
        WebDriverWait(driver, 20).until(
            lambda d: d.current_url != url,
            "Aura Failed To bypass"
        )
        
        final_url = driver.current_url
        return {"status": "Bypassed Url", "bypassed_url": final_url}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    finally:
        driver.quit()


@app.route('/bypass', methods=['POST'])
def bypass_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"status": "error", "message": "Please provide a URL in JSON format"}), 400
    
    url = data['url']
    result = bypass_shortner_in_headless(url)
    return jsonify(result)


@app.route('/')
def home():
    return "Aura Bypass Bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT env var
    app.run(host='0.0.0.0', port=port)
