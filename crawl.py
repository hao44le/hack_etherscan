from bs4 import BeautifulSoup
import sys
from re import sub
from decimal import Decimal
import datetime
import re
import urllib2
from dateutil import parser
from model import TokenTransaction
def get_html_by_url(url):
    # Your code where you can use urlopen
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_transcripts_at_p(token_name,p):
  base_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0xe41d2489571d322189246dafa5ebde1f4699f498&p={}'.format(p)
  soup = get_html_by_url(base_url)
  arrs = soup.findAll('tr')
  transactions = []
  for x in range(1,len(arrs)):
    arr = arrs[x]
    tds = arr.findAll('td')
    txhash = ""
    timestamp = ""
    from_account = ""
    to_account = ""
    quantity = ""
    for y in range(0,len(tds)):
       td = tds[y]
       if y == 0:
         #txhash
         txhash = td.text
       elif y == 1:
         #timestamp
         timestamp = td.find("span")["title"]
         timestamp = parser.parse(timestamp)
       elif y == 2:
         #from
         from_account = td.find("span").find('a').text
       elif y == 4:
         # to
         to_account = td.find("span").find("a").text
       elif y == 5:
         # quantity
         quantity = td.text
    token_transaction = TokenTransaction(token_name,txhash,timestamp,from_account,to_account,quantity)
    transactions.append(token_transaction)
  return transactions


def write_to_csv(transactions):
  csvoutput = open("0x.csv","w+")
  csvoutput.write("Token_Name\ttxhash\ttimestamp\tfrom_account\tto_account quantity\n")
  for t in transactions:
    csvoutput.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(t.token_name,t.tx_hash,t.timestamp,t.from_account,t.to_account,t.quantity))
  csvoutput.close()

total = []
for x in range(1,2452):
  print(x)
  transactions = get_transcripts_at_p("0x",x)
  total = total + transactions
write_to_csv(total)
