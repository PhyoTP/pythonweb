from flask import Blueprint, request, Response
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
# chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
# chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
# chrome_options.add_argument("--disable-gpu")  # Disable GPU (if not needed)

bp = Blueprint("stickynotes", __name__, template_folder='templates')

def get_dynamic_content(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(2)  # Wait for JS to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        driver.quit()


@bp.route('/stickynotes/ask', methods=['GET'])
def find_coupons():
    website = request.args.get('w')
    if not website:
        return "No URL provided", 400
    
    try:
        # Create a streaming completion
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Verify model name
            messages=[
                {
                    "role": "system",
                    "content": "Can you search the web to find every coupon you can for the website specified by the user separated by commas? Please put all the codes you can find like this: HELLO15, EXAMPLE23"
                },
                {
                    "role": "user",
                    "content": website
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Stream the response
        def generate():
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                yield content
        
        return Response(generate(), content_type='text/plain')
    
    except Exception as e:
        return {"error": str(e)}, 500
# @bp.route('/stickynotes/ask', methods=['GET'])
# def find_coupons():
#     website = request.args.get('w')
#     if not website:
#         return "No URL provided", 400

#     try:
#         response = requests.get(
#             f"https://www.googleapis.com/customsearch/v1?q=site%3Acoupons.slickdeals.net+OR+site%3Arakuten.com+OR+site%3Aozbargain.com.au+OR+site%3Acouponese.com+OR+site%3Acouponzguru.sg+{website}+discount+OR+coupon+code&key=AIzaSyB4PrFo2t1SprGstVveXpIJjAjCCokOz-M&cx=5735dd201233b4cc3",
#             timeout=10
#         )
#         response.raise_for_status()
#         urls = [i["link"] for i in response.json().get("items", [])]
#     except (requests.exceptions.RequestException, KeyError) as e:
#         print("Failed to fetch URLs:", e)
#         urls = []

#     all_coupons = set()

#     for url in urls:
#         soup = get_dynamic_content(url)
#         if not soup:
#             continue
#         print(url)
#         if "coupons.slickdeals.net" in url:
#             print("Slick Deals:")
#             elements = soup.find_all('div', class_="_1ip0fbd5", attrs={"data-attribute": "code"})
#             data_ids = [element.get('data-id') for element in elements if element.get('data-id')]
#             print("Data ids:", data_ids)
#             coupons = []
#             for i in data_ids:
#                 try:
#                     coupon_response = requests.get(
#                         f'https://coupons.slickdeals.net/api/voucher/country/us/client/a1cf309737e64efba2197ca0d5820b5f/id/{i}',
#                         timeout=10
#                     )
#                     coupon_response.raise_for_status()
#                     coupons.append(coupon_response.json().get("code", ""))
#                 except (requests.exceptions.RequestException, KeyError) as e:
#                     print("Failed to fetch Slick Deals coupon:", e)
#             print(coupons)
#             all_coupons.update(coupons)

#         elif "rakuten.com" in url:
#             print("Rakuten:")
#             coupons = [i.get_text(strip=True) for i in soup.find_all('span', class_="promo-code")]
#             print(coupons)
#             all_coupons.update(coupons)

#         elif "ozbargain.com.au" in url:
#             print("Oz Bargain:")
#             driver = webdriver.Chrome(options=chrome_options)
#             driver.get(url)
#             blocks = driver.find_elements(By.CLASS_NAME, 'couponcode')
#             # Extract valid coupons from strong tags
#             coupons = []
#             for block in blocks:
#                 if 'line-through' not in block.value_of_css_property('text-decoration'):
#                     strong_elements = block.find_elements(By.TAG_NAME, 'strong')
#                     for strong in strong_elements:
#                         coupons.append(strong.text.strip())
#             print(coupons)
#             all_coupons.update(coupons)
#             driver.quit()
#         elif "couponese.com" in url and url != "https://www.couponese.com/":
#             print("Couponese:")
#             driver = webdriver.Chrome(options=chrome_options)
#             driver.get(url)
#             blocks = driver.find_elements(By.CLASS_NAME, 'ov-code')
#             coupons = [
#                 block.text for block in blocks
#                 if 'line-through' not in block.value_of_css_property('text-decoration')
#             ]
#             print(coupons)
#             all_coupons.update(coupons)
#             driver.quit()
#         elif "couponzguru.sg" in url:
#             print("Couponzguru:")
#             coupons = [i.get_text(strip=True) for i in soup.find_all('span', class_="clicktoreveal-code") if i.get_text(strip=True) != "Deal Activated"]
#             print(coupons)
#             all_coupons.update(coupons)
#     print("\nAll Coupons Collected:")
#     print(all_coupons)
#     return list(all_coupons)
