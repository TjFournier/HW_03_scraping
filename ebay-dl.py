import argparse
import requests
from bs4 import BeautifulSoup
import json


# Makes sure hotness only returns a number
def parse_itemssold(text):
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

if __name__ == '__main__':
    
    # Get command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages',default=10)
    args = parser.parse_args()
    print('args.search_terms=', args.search_term)

    items = []
    for page_number in range(1, int(args.num_pages)+1):
        #Build the URL
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=' 
        url += args.search_term 
        url += '&_sacat=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print('url=',url)

        # download the HTML
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html = r.text
        #print('html=', html[:50])

        # process the html
        
        soup = BeautifulSoup(html, 'html.parser')

        tags_items = soup.select('.s-item')
        for tag_item in tags_items:
            # print('tag_itme=',tag_item)
            
            # Extract the name
            tags_name = tag_item.select('.s-item__title')
            name = None
            for tag in tags_name:
                name = tag.text

            # Extract the price
            tags_name = tag_item.select('.s-item__price')
            price = None
            for tag in tags_name:
                price = tag.text

            # Extract the item condition
            tags_name = tag_item.select('.s-item__subtitle')
            item_condition = None
            for tag in tags_name:
                item_condition = tag.text

            # Extract the shipping price
            tags_name = tag_item.select('.s-item__shipping')
            shipping_price = 0
            for tag in tags_name:
                shipping_price = tag.text

            # Extract the free returns
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            # Extract the the number of items sold
            tags_name = tag_item.select('.s-item__hotness')
            items_sold = 0
            for tag in tags_name:
                items_sold = parse_itemssold(tag.text)

            item = {
                'name': name,
                'price': price,
                'status': item_condition,
                'shipping_price': shipping_price,
                'free_returns': freereturns,
                'items_sold': items_sold,
            }
            items.append(item)

        print('len(tag_items)=',len(tags_items))
        print('len(items)', len(items))

    # Write the json into a file
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))