import argparse

parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
parser.add_argument('search_term')

args = parser.parse_args()
print('args.search_terms=', args.search_term)