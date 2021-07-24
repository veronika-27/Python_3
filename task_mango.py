from requests_html import HTMLSession
import re
import json

session = HTMLSession()

# Requesting the page
resp = session.get("https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99&fbclid=IwAR1VV0mSDfU4cqiE73mN7POAQxTcwPJajK0MZvj1M9IL_76oXRiEteMjFC0")

# Render JavaScript
resp.html.render(timeout = 30.0)

#Collecting the data needed
product_name = resp.html.find('h1.product-name', first = True).text
product_sale_price = resp.html.find('span.product-sale', first = True).text
price = float(re.findall(r"\d*\.\d*",product_sale_price)[0])
product_color = resp.html.find('.color-container--selected', first = True)
selected_color = product_color.attrs['aria-label'].split()[0]
product_sizes = resp.html.find('span.size-available')
available_sizes = []
for el in product_sizes:
    if el.attrs['data-available'] == 'true':
        available_sizes.append(el.attrs['data-size'])

#Output the data as JSON
final_dict = {
    'name' : product_name,
    'price' : price,
    'color' : selected_color,
    'size' : available_sizes
    }
print(json.dumps(final_dict))
