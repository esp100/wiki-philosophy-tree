import src.config as config
import requests 
from bs4 import BeautifulSoup 


def clean_html_parentheses(html_string):
  result = []
  parentheses_depth = 0
  in_tag = False

  for char in html_string:
    if char == '<':
      in_tag = True

    if not in_tag:
      if char == '(':
        parentheses_depth += 1
        continue
      elif char == ')':
        parentheses_depth -= 1
        continue
    if parentheses_depth == 0:
      result.append(char)

    if char == '>':
      in_tag = False

  return ''.join(result)

def get_next_page(page):

  full_url = config.BASE_URL + page
  try:
    response = requests.get(full_url, headers=config.BASE_HEADERS, timeout=10)
    response.raise_for_status()
  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err} for {full_url}")
    return None
  except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err} for {full_url}")
    return None
  except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err} for {full_url}")
    return None
  except Exception as err:
    print(f"An unexpected error occurred: {err} for {full_url}")
    return None

  soup = BeautifulSoup(response.text, "html.parser")
  first_section = soup.find("section", attrs={"data-mw-section-id" : "0"})

  if not first_section:
    print(f"No first content section found for page: {page}")
    return None

  for infocards in first_section.find_all("table"):
    infocards.decompose()
  for references in first_section.find_all("sup", attrs={"rel":"dc:references"}):
    references.decompose()

  paraphs = first_section.select('p[id]')
  for paraph in paraphs:
    cleaned_paraph_html = clean_html_parentheses(str(paraph))
    cleaned_paraph = BeautifulSoup(cleaned_paraph_html, "html.parser")

    links_in_paraph = cleaned_paraph.select('a[id]', href=True)
    if links_in_paraph:
      for link in links_in_paraph:
        next = link.get("href")

        if next.endswith('?action=edit&redlink=1'):
          continue
        else:
          substracted_page = "/"+next.split("/")[-1]
          
          return substracted_page

  return None

def all_the_ways_lead_to(starting_page):
  
  route = []
  route.append(starting_page)
  failsafe = 0
  while route[-1] != config.TARGET:
    route.append(get_next_page(route[-1]))
    failsafe += 1
    if failsafe > config.FAILSAFE:
      print("stoped before target")
      break
  return route