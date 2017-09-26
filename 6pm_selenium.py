import requests
from lxml import etree
from fake_useragent import UserAgent
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

ua = UserAgent()
header = {
	'Host':'www.6pm.com',
	'User-Agent':ua.random,
	'Upgrade-Insecure-Requests':'1'
	}


def get_info(url):
	description = []
	data = {}
	SKU = []


	# stocks = {}
	try:
		browser = webdriver.PhantomJS(executable_path= r"D:\D\python\book\selenium\phantomjs.exe")
		#browser = webdriver.Chrome()
		browser.get(url)
		browser.maximize_window()
		
		# 标题
		try:
			title = browser.find_element_by_xpath("/html/head//title").get_attribute('text')
			#for title in titles:
			#print(title)
		except:
			title = ""
			print("title获取失败")

		#id
		try:
			productId = browser.find_element_by_xpath("//meta[@name='branch:deeplink:product']").get_attribute('content')
			#print(productId)
		except:
			print("获取商品id失败")

		# 品牌
		try:
			brand = browser.find_element_by_xpath("//span[@itemprop='brand']").text
			#print(brand)
		except:
			brand = ""
			print("brand获取失败")

		# 价格
		try:
			price = browser.find_element_by_xpath("//div[@class = '_7Ri0r']//span[@class='_3r_Ou ']").text
			#print(price)
		except:
			price = ""
			print("price获取失败")

		# 产品信息
		try:
			div = browser.find_element_by_xpath("//div[@class='_3iH0n']")
			
			lis = div.find_elements_by_tag_name("li")
			for li in lis:
				description.append(li.text)

			ul = browser.find_element_by_xpath("//div[@class='_1Srfn']/ul")
			liss = ul.find_elements_by_xpath("li")
			for ls in liss:
				description.append(ls.text)
				#print(ls.text)
		 		
			#print(description)

		except Exception as e:
		 	description = [""]
		 	print("description获取失败--{}".format(e))
		
		# 获取库存量
		#color熟悉是否存在
		try:
			colors_label = browser.find_element_by_xpath("//div[@class='_7Ri0r']//label[@for='pdp-color-select']").text
		except:
			colors_label = ""
		if colors_label:
			try:
				colors = Select(browser.find_element_by_xpath("//div[@class='_7Ri0r']//select[@id='pdp-color-select']"))
			except:
				colors = browser.find_element_by_xpath("//div[@class='_7Ri0r']//label[@for='pdp-color-select']/../div").text
			#print(type(colors))
		else:
			colors = ""

		# size属性是在存在
		try:
		 	sizes_label = browser.find_element_by_xpath("//div[@class='_7Ri0r']//label[@for='pdp-size-select']").text
		except:
		 	sizes_label = ""
		#print(sizes_label)
		if sizes_label:
		  	try:
		  		sizes = Select(browser.find_element_by_xpath("//div[@class='_7Ri0r']//select[@id='pdp-size-select']"))
		  	except:
		  		sizes = browser.find_element_by_xpath("//div[@class='_7Ri0r']//label[@for='pdp-size-select']/../div").text
		  	#print(type(sizes))
		else:
			sizes = ""

		# 判断是否存在width
		try:
			widths_label = browser.find_element_by_xpath("//div[@class='_7Ri0r']//label[@for='pdp-width-select']").text
		except:
			widths_label = ""
		if widths_label:
			try:
				widths = Select(browser.find_element_by_xpath("//div[@class='_7Ri0r']//select[@id='pdp-width-select']"))
			except:
				widths = browser.find_element_by_xpath("//div[@class='_7Ri0r']//label[@for='pdp-width-select']/../div").text
			#print(type(widths))
			# print(len(colors.options),len(sizes.options),len(widths.options))
		else:
			widths = ""
		
		csw = [{'name':colors_label,'values':colors,'typ':'color'},
			{'name':sizes_label,'values':sizes,'typ':'size'},
			{'name':widths_label,'values':widths,'typ':'width'}]
		lists,str_lists = check_type(csw)
		# print(str_lists)
		if len(lists) == 0:
			try:
				stock = browser.find_element_by_xpath("//div[@class='_7Ri0r']//button[@class='_1HQVd']").text
			except Exception as e:
				stock = ""
				print(e)
			SKU.append({colors_label:colors,sizes_label:sizes,widths_label:widths,'stock':stock})
		else:
			for color in lists[0]['values']:
				color.click()
				#print(color.text)
				#time.sleep(1)
				try:
					for size in lists[1]['values']:
						size.click()
						#print(size.text)
						#time.sleep(2)

						try:
							for width in lists[2]['values']:
								width.click()
								#print(width.text)
								try:
									stock = browser.find_element_by_xpath("//div[@class='_7Ri0r']//div[@class='_1rUc_']").text
								except:
									stock = browser.find_element_by_xpath("//div[@class='_7Ri0r']//button[@class='_1HQVd']").text
								SKU.append({lists[0]['name']:color.text,lists[1]['name']:size.text,lists[2]['name']:width.text,'stock':stock})
						except:
							try:
								stock = browser.find_element_by_xpath("//div[@class='_7Ri0r']//div[@class='_1rUc_']").text
							except:
								stock = browser.find_element_by_xpath("//div[@class='_7Ri0r']//button[@class='_1HQVd']").text
							
							SKU.append({lists[0]['name']:color.text,lists[1]['name']:size.text,str_lists[0]['name']:str_lists[0]['values'],'stock':stock})

				except:
					try:
						stock = browser.find_element_by_xpath("//div[@class='_7Ri0r']//div[@class='_1rUc_']").text
					except:
						stock = browser.find_element_by_xpath("//div[@class='_7Ri0r']//button[@class='_1HQVd']").text
					SKU.append({lists[0]['name']:color.text,str_lists[0]['name']:str_lists[0]['values'],str_lists[1]['name']:str_lists[1]['values'],'stock':stock})
		data['title'] = title
		data['productId'] = productId 
		data['brand'] = brand 
		data['price'] = price
		data['description'] = description
		data['SKU'] = SKU

	except Exception as e:
		print("出错了，{}".format(e))
	finally:
		browser.close()
		browser.quit()
		return data


def check_type(attributes):
	"""判断该商品的是否含属性值，如不存在属性或属性为一，则不需要遍历"""
	try:
		select_lists = []
		str_lists = []
		for attribute in attributes:
			if isinstance(attribute['values'],Select):
				if attribute['typ'] == 'color':
					attribute['values'] = attribute['values'].options
				else:
					attribute['values'] = attribute['values'].options[1:]
				select_lists.append(attribute)
			# elif isinstance(attribute['values'],str):
			# 	str_lists.append(attribute)
			else:
				str_lists.append(attribute)
	except Exception as e:
		print('检查类型出错了{}'.format(e))

	return select_lists,str_lists


def get_html(url):
	'''获取商品详情页html'''
	try:
		r = requests.get(url,headers= header,timeout=30)
		r.raise_for_status()
		r.apparent_status = r.status_code
		return r.text
	except:
		print("获取页面失败")


def get_img(data):
	'''获取商品详情页html'''
	productId = data['productId']
	# 获取商品的不同颜色的images地址，可用于下载
	img_url = 'https://api.zcloudcat.com/v1/images?productId={}&siteId=2&recipe=["MULTIVIEW","SWATCH"]&type=["SWATCH","PAIR","TOP","BOTTOM","LEFT","BACK","RIGHT","FRONT"]&excludes=["format","productId","recipeName","styleId","imageId"]'.format(productId)
	try:
		img_urls = get_html(img_url)
		img_content = json.loads(img_urls)
		images = img_content['images']
		data['images'] = images
	except:
		print("获取商品不同颜色images失败")
	return data

	
def output_json(data):
	"""将数据保存至json"""
	print(json.dumps(data, sort_keys=True, indent=4))
	# choice = input("是否保存至6pm.json？y/n: ")
	# if choice == 'y':
	with open('./6pm.json', 'a+') as fp:
		json.dump(data, fp, indent=4)
		print("数据保存至6pm.json成功")


def test():
	'''测试'''
	# "https://www.6pm.com/p/lifestride-spark-red/product/8872328/color/585" # color:n, size:n, width:n
	# "https://www.6pm.com/p/ugg-kids-tesni-fair-isle-little-kid-big-kid-cosmic/product/8654843/color/162672" #color:1, size:1, width:1
	# 'https://www.6pm.com/p/vince-camuto-korthina-moonlight-mexico/product/8877560/color/687159' # color:n, size:n, width:1
	# 'https://www.6pm.com/p/coach-tatum-green-gold-silver/product/8976455/color/722032' # color：n,size:0, width:0
	# 'https://www.6pm.com/p/pearl-izumi-select-persuit-jersey-black-lime-punch/product/9017093/color/29068' color:1,size:n,width:0
	urls = ["https://www.6pm.com/p/lifestride-spark-red/product/8872328/color/585", # color:n, size:n, width:n,
			"https://www.6pm.com/p/ugg-kids-tesni-fair-isle-little-kid-big-kid-cosmic/product/8654843/color/162672", #color:1, size:1, width:1,
			'https://www.6pm.com/p/vince-camuto-korthina-moonlight-mexico/product/8877560/color/687159', # color:n, size:n, width:1,
			'https://www.6pm.com/p/coach-tatum-green-gold-silver/product/8976455/color/722032', # color：n,size:0, width:0,
			'https://www.6pm.com/p/pearl-izumi-select-persuit-jersey-black-lime-punch/product/9017093/color/29068']
	
	for url in urls:
		try:
			data = get_info(url)
			data = get_img(data)
			output_json(data)
		except Exception as e:
			print(e)
			continue


def main(url):
	try:
		data = get_info(url)
		data = get_img(data)
		output_json(data)
	except Exception as e:
		print(e)

if __name__ == '__main__':
 	test()
