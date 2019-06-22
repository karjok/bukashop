
# BukaShop
# Karjok Pangesty
# 22 juni 2019
# CANTUMKAN SUMBER !!


from requests import *
from bs4 import BeautifulSoup as bs
from json import *
from threading import Thread as t
import os,re,sys,time

data =[]
h = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def bl(q):
	# top 100 by relevanity
	base = 'https://m.bukalapak.com'
	urls = [base+'/products?keywords='+q+'&search[sort_by]=_score:desc']
	no = 0
	while True:
		if len(data) == 100:
			break
		try:
			r = get(urls[no]).text
			b = bs(r,'html.parser')
			no += 1
			for i in b.find_all('article'):
				if len(data) == 100:
					break
				url = base+i.get('data-url')
				nama = i.get('data-name')
				harga = i.find('div',{'class':'product-price'}).get('data-reduced-price')
				toko = '\033[95mBukalapak\033[0m'
				data.append((int(harga),nama,url,toko))
			urls.append(base+b.find('a',{'class':'next_page'}).get('href'))
		except:
			break
def sp(q):
	q = q.replace(' ','%20')
	r = get('https://shopee.co.id/api/v2/search_items/?by=relevancy&keyword='+q+'&limit=100&newest=0&order=desc&page_type=search',headers=h).json()
	go = [(i['itemid'],i['shopid']) for i in r['items']]
	from multiprocessing.pool import ThreadPool as tp
	t = tp(10)
	def ss(r):
		rr = get(f'https://shopee.co.id/api/v2/item/get?itemid={r[0]}&shopid={r[1]}').json()
		url = f'https://shopee.co.id/product-i.{r[1]}.{r[0]}'
		harga = round(rr['item']['price']/100000)
		nama = rr['item']['name']
		toko = '\033[93mShopee\033[0m'
		data.append((harga,nama,url,toko))	
#		print(f'\rShopee {len(data)}',end=''),;sys.stdout.flush()
	p = t.map(ss,go)
	
def comp():
	''' Ini fungsi ter ajg yg pernah w buat :"V Tapi ya bodoamat lah ajg :*'''
	bl(q)
	sp(q)

def ahah():
	data.sort()
	for i in data:
			print(f'''Produk : {i[1]}
Harga  : Rp{i[0]}
Toko   : {i[3]}
URL    : \033[90m{i[2]}\033[0m
++++++++++++++++++++++++++++++++++++++
''')
	print(f'''####################################################
Harga terendah  : \033[92mRp{data[0][0]}\033[0m ({data[0][3]})
Harga tertinggi : \033[91mRp{data[-1][0]}\033[0m ({data[-1][3]})''')	
if __name__=='__main__':
	os.system('clear')
	print('''\033[95m
     _          \033[0m __       _ \033[95m
    |_)    |  _ \033[0m(_ |_  _ |_)\033[95m
    |_)|_| |<(_|\033[0m__)| |(_)|  \033[95mfb.me/om.karjok
    |\033[0mBukalapak x Shopee price sorter
    ''')
	q = input('Cari : ')
	tr = t(target=comp,name='tmp')
	tr.start()
	txt = ['   ','.  ','.. ','...']
	while tr.isAlive():
		for i in txt:
			print(f'\rSedang nyariin {q} buat kamu{i}',end=''),;sys.stdout.flush();time.sleep(0.5)
	
	print('\n')
	ahah()
