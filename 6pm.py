import requests
from lxml import etree
from fake_useragent import UserAgent
import json
import pandas


ua = UserAgent()
header = {
	'Host':'www.6pm.com',
	'User-Agent':ua.random,
	'Upgrade-Insecure-Requests':'1'
	}


def get_html(url):
	'''获取商品详情页html'''
	try:
		r = requests.get(url,headers= header,timeout=30)
		r.raise_for_status()
		r.apparent_status = r.status_code
		return r.text
	except:
		print("获取页面失败")


def parser(html_content):
	'''解析页面，获得标题、品牌、价格、产品信息，图片下载地址'''
	selector = etree.HTML(html_content)
	infos = []
	data = []
	
	# 标题
	try:
		title = selector.xpath("//title/text()")[0]
		print(title)
	except:
		title = ""
		print("title获取失败")
	# 品牌
	try:
		brand = selector.xpath("//meta[@name='og:title']/@content")[0].split(' ')[0]
		print(brand)
	except:
		brand = ""
		print("brand获取失败")

	# 价格
	try:
		price = selector.xpath("//span[@class='_3r_Ou ']/text()")[0]
		print(price)
	except:
		price = ""
		print("price获取失败")

	# 产品信息
	try:
		lis = selector.xpath("//div[@class='_1Srfn']/ul/div//li")
		for li in lis:
			li = "".join(li.xpath(".//text()"))
		liss = selector.xpath("//div[@class='_1Srfn']/ul/li")
		for ls in liss:
			infos.append("".join(ls.xpath(".//text()")))
		description = li+"   "+'   '.join(infos)
		print(description)
	except:
		description = ""
		print("description获取失败")
	
	# 商品的颜色
	try:
		key1 = "".join(selector.xpath("//div[@class='_1EOb4']//div[@class='_17Dby'][1]/form/div[1]/label//text()"))
		value1 = ",".join(selector.xpath("//div[@class='_1EOb4']//div[@class='_17Dby'][1]/form/div[1]/div//text()"))
		color = {key1:value1}
		print(color)
	except:
		print("color获取失败")

	# 商品可能存在的size
	try:
		key2 = "".join(selector.xpath("//div[@class='_1EOb4']//div[@class='_1KSLq']/div[1]//label//text()"))
		value2 = ",".join(selector.xpath("//div[@class='_1EOb4']//div[@class='_1KSLq']/div[1]//select/option[position()>1]//text()"))
		
		size = {key2:value2}
		print(size)
	except:
		print("size获取失败")

	# 商品可能存在的width
	try:
		key3 = "".join(selector.xpath("//div[@class='_1EOb4']//div[@class='_1KSLq']/div[2]//label//text()"))
		value3 = ",".join(selector.xpath("//div[@class='_1EOb4']//div[@class='_1KSLq']/div[2]//select/option[position()>1]//text()"))
		width = {key3:value3}
		print(width)
	except:
		print("width")
	#id
	try:
		productId = selector.xpath("//meta[@name='branch:deeplink:product']/@content")[0]
	except:
		print("获取商品id失败")

	# 获取商品的不同颜色的images地址，可用于下载
	img_url = 'https://api.zcloudcat.com/v1/images?productId={}&siteId=2&recipe=["MULTIVIEW","SWATCH"]&type=["SWATCH","PAIR","TOP","BOTTOM","LEFT","BACK","RIGHT","FRONT"]&excludes=["format","productId","recipeName","styleId","imageId"]'.format(productId)
	try:
		img_urls = get_html(img_url)
		img_content = json.loads(img_urls)
		images = img_content['images']
		print(images)
	except:
		print("获取商品不同颜色images失败")
	data.append([title,brand,price,description,value1,value2,value3,images])
	return data


def output_excel(data):
	choice = input("是否愿意保存至excel？y/n: ")
	if choice == 'y':
		try:
			df = pandas.DataFrame(data)
			df.to_excel(r"./6pm.xlsx", sheet_name='商品详情信息')
			print("数据保存至excel成功！")
		except:
			print("数据保存至excel失败！")
	else:
		return
		

def test():
	url = 'https://www.6pm.com/p/lifestride-spark-red/product/8872328/color/585'
	try:
		html_content = get_html(url)
		# with open('./6pm.html','wb') as f:
		# 	f.write(html_content.encode('utf-8'))
		data = parser(html_content)
		output_excel(data)
	except Exception as e:
		print(e)


def main():
	url = input("请输入商品详情页地址：")
	try:
		html_content = get_html(url)
		data = parser(html_content)
		output_excel(data)
	except Exception as e:
		print(e)


if __name__ == '__main__':
	test()
