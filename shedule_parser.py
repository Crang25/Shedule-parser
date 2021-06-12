from fake_useragent import UserAgent
from shutil import get_terminal_size
from json import loads
from os import system
import requests
import re

import config

assert config.GROUPS not in (None, ''), 'GROUPS must be created in config.py'
assert config.MAIN_URL not in (None, ''), 'MAIN_URL must be created in config.py'
assert config.DAY_URL not in (None, ''), 'DAY_URL must be created in config.py'
assert config.HOST not in (None, ''), 'HOST must be created in config.py'

groups = config.GROUPS
main_url = config.MAIN_URL
day_url = config.DAY_URL
max_len = get_terminal_size((110, 30)).columns

def program_exit():
	input('Нажмите что-нибудь, чтобы выйти...')
	quit()

def display_week(table_ls, week):
	couple = table_ls[0][1:]
	times = table_ls[1][1:]
	
	sepr = '.' * max_len
	star_sepr = '*' * max_len

	print(f'\n{week}, неделя')
	for i in table_ls[2:]:
		day = [j for j in i[1:]]
		print(f'\n{star_sepr}\n{i[0]}\n')
		for k in range(0, len(couple)):
			print(f"{sepr}\n{couple[k]} пара, с {times[k].split('-')[0]} до {times[k].split('-')[1]}")
			if(day[k] == ''):
				print(f'Нет\n{sepr}\n')
				continue
			print(f'{day[k]}\n{sepr}\n')
		print(star_sepr)

def get_day(table_ls, date):
	'''Функция, которая выводит расписание на день "date"
	:param: table_ls: Список со списками строк таблицы
	:type table_list: list
	:param str date: Строка - дата искомой недели
	'''

	couple = table_ls[0][1:]
	times = table_ls[1][1:]
	
	# Search for a date in the schedule
	day = [i[1:] for i in table_ls[2::] if ' '.join(i[0].split(',')[1].split(' ')[0::2]).lower() == date.lower()][0]
	
	sepr = '.' * max_len
	
	print(f'\n{date.lower()}')
	for i in range(0, len(couple)):
		print(f"\n{sepr}")
		print(f"{couple[i]} пара, с {times[i].split('-')[0]} до {times[i].split('-')[1]}")
		if(day[i]==''):
			print(f'Нет\n{sepr}')
			continue
		print(day[i])
		print(sepr)

def get_content(url):
	proxies = {
		'SOCKS5':'184.185.2.146:47659', #USA NY
		# 'SOCKS5':'96.44.183.149:55225', #USA LS
		'HTTPS':'176.115.197.118:8080' #Russia Mcw
	}

	u = UserAgent()
	#Random User_Agent
	ua = u.random

	# Url main page
	refer = main_url.replace('?group=', 'static/index.html')
	headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'Connection': 'keep-alive',
		'DNT': '1',
		'Host': config.HOST,
		'Referer': refer,
		'User-Agent' : str(ua)
	}

	return requests.get(url, headers=headers, proxies=proxies).content

def get_week(url, group):
	table = loads(get_content(url))
	
	# Quantity of weeks
	weeks = table['weeks']
	print('Возможные недели:\n', *weeks)
	week = int(input('\nВведите номер искомой недели: '))
	if(week not in weeks):
		print('Такой недели нет, попробуйте ещё раз')
		program_exit()
	
	table = loads(get_content(main_url+str(groups[group])+day_url+str(week)))
	#List with lists rows
	data = table['table']['table']
	display_week(data, week)

def search_day(url, group):
	jsons = loads(get_content(url))
	weeks = jsons['weeks']
	# check = '23 мая 1 сентября 6 марта'
	print("Введите день в формате: 'день месяца название месяца(в родительном падеже)\nПример: 14 апреля")
	day = input(": ")
	pattern = re.findall(r'(\d+) (января|февраля|марта|апреля|мая|июня|июля|сентября|октября|ноября|декабря)', day)
	if(len(pattern) == 0):
		print('Такой даты нет')
		quit()
	day = (pattern[0][0] + ' '+ pattern[0][1]).lower()
	
	print('Поиск даты...')
	search_group, k = groups[group], 0
	for i in weeks:
		new_url = main_url + str(search_group) + day_url + str(i)
		new_json = loads(get_content(new_url))
		new_table = new_json['table']['table'][2:]
		new_day = ''
		
		for j in new_table:
			new_day = ' '.join(j[0].split(',')[1].split(' ')[0::2])
			if(new_day == day):
				get_day(new_json['table']['table'], day)
				k = 1
				break
	if(k == 0):
		print('Ничего не найдено')
		program_exit()

def display_current_week(url):
	table = loads(get_content(url))['table']
	couple = table['table'][0][1:]
	times = table['table'][1][1:]
	week =table['week']
	
	sepr = '.' * max_len
	star_sepr = '*' * max_len

	print(f'\n{week}, неделя')
	for i in table['table'][2:]:
		day = [j for j in i[1:]]
		print(f'\n{star_sepr}\n{i[0]}\n')
		for k in range(0, len(couple)):
			print(f"{sepr}\n{couple[k]} пара, с {times[k].split('-')[0]} до {times[k].split('-')[1]}")
			if(day[k] == ''):
				print(f'Нет\n{sepr}\n')
				continue
			print(f'{day[k]}\n{sepr}\n')
		print(star_sepr)

def main():
	# Url from which a server request is generated 
	base_url = main_url.replace('group', 'query')

	system('cls')
	choose = int(input('1 - Вывести расписание на неделю\n2 -  Вывести расписание на один день\n3 - Вывести расписание на текущую неделю\n:'))
	if(choose!=1 and choose !=2 and choose!=3):
		quit()

	#Group name
	group = input('Введите имя искомой группы: ').lower()
	if(group not in groups):
		print('Такой группы нет в списке, либо ее еще не добавили в программу')
		program_exit()
	if(choose == 1):
		get_week(base_url+group, group)
		program_exit()
	elif(choose == 2):
		search_day(base_url+group, group)
		program_exit()
	else:
		display_current_week(base_url+group)
		program_exit()
if __name__=='__main__':
	main()