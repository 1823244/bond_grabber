# Граббинг купонов для облигаций с сайта bonds.finam.ru

Скрипт формирует файл в формате json с данными о купонах выбранной облигации.  
Поиск облигации ведется по ISIN.  

### Использование

Запустить скрипт с параметрами:  
```
$> python get_bonds.py XS0114288789 c:\bonds
$> python get_bonds.py XS0114288789 "c:\rus state bonds"
```
Параметры (позиционные, отделяются пробелом):  
1. ISIN  
2. Путь к каталогу выгрузки. Если есть пробелы - его следует заключить в кавычки. Не должен заканчиваться на '\'.  

Если путь не указан, то файлы с результатами будут созданы в текущем каталоге скрипта.  
Формат имен файлов:  
```
ISIN_coupons.json
```
где ISIN заменяется на значение из первого параметра.  

## Немного теории.

Купоны на сайте bonds.finam.ru лежат по ссылкам, не имеиющим в своем пути ISIN, поэтому их приходится искать.  
Для поиска отправляется запрос GET следующего формата:  
```
https://bonds.finam.ru/issue/search/default.asp?emitterCustomName=XS0114288789
```
Результатом функции поиска является ссылка вида:  
```
https://bonds.finam.ru/issue/details001D6/default.asp
```
в которой ключевым  полем является _details001D6_   
Для получения ссылки на страницу с купонами надо добавить '00002' к этому полю, чтобы получилось так:  
```
https://bonds.finam.ru/issue/details001D600002/default.asp
```

## Разное.

https://realpython.com/python-web-scraping-practical-introduction/

preparation

python -m venv bonds_grabber    
cd venv/Scripts  
activate.bat  
pip install requests BeautifulSoup4 bs4  
