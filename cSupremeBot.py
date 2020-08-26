from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By

# Вот так должен выглядеть словарь, закидываемый в subDirs
#
# items = {
#               "/jackets": [{"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"}],
#               "/shirts": [{"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"}],
#               "/tops_sweaters": [{"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"}],
#               "/sweatshirts": [{"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"}],
#               "/pants": [{"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"}],
#               "/shorts": [{"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"}]
# }

KEY = 0
VALUE = 1
HOME = 'https://www.supremenewyork.com/shop/all'


class SupremeBot:

    subDirs = {}  # Словарь с элементами для поиска
    currentPage = ""

    def __init__(self, itemsList):
        # Конструктор
        self.driver = webdriver.Firefox();
        self.subDirs = itemsList

    def goTo(self, href):
        # Переходит по ссылке
        self.driver.get(href)
        self.currentPage = href

    def searchAll(self):
        # Находит все элементы в каждом значении словаря subDirs
        for dirs in self.subDirs.items():
            if dirs[VALUE]:
                self.goTo(HOME + dirs[KEY])
                allItems = self.findMany()
                for desirable in dirs[VALUE]:
                    self.goTo(self.findPerfectMatch(allItems, desirable))
                    sizes = self.driver.find_elements_by_tag_name("option")
                    self.getPerfectItem(sizes, desirable["size"])
            else:
                continue

    def getPerfectItem(self, sizes, desirableSize):
        # Кидает в корзину найденный элемент нужного размера
        for size in sizes:
            if size.text == desirableSize:
                size.click()
                break
            else:
                continue
        self.driver.find_element_by_name("commit").click()

    def getFirstItem(self):
        # Кидает в корзину элемент стокового размера. Обычно - М
        self.driver.find_element_by_name("commit").click()

    def goToCheckOut(self):
        self.goTo("https://www.supremenewyork.com/checkout")

    def findMany(self):
        # Возвращает список из словарей для каждого товара на странице
        # Первый элемент - словарь с названием и цветом, второй - ссылка, чтобы перейти
        # {"element": {"NAME": "value", "COLOR": "value"}, "LINK": "value"}
        elements = []

        for item in self.driver.find_elements_by_class_name("inner-article"):
            element = {"element": {"name": "", "color": ""}, "link": ""}
            key = "name"
            for data in item.find_elements_by_class_name("name-link"):
                element["element"][key] = data.text
                key = "color"
            element["link"] = item.find_element_by_class_name("name-link").get_attribute("href")
            elements.append(element)

        return elements

    def findPerfectMatch(self, elements, desirable):
        # Принимает список элементов типа как из функции findMany
        # В качестве желаемого принимает словарь из таких ключей, как NAME, COLOR, SIZE
        # Возвращает ссылку на желаемый элемент
        for element in elements:
            if (element["element"]["name"] == desirable["name"]) & (element["element"]["color"] == desirable["color"]):
                return element["link"]
            else:
                continue

    def findFirstMatch(self, desirable, page, anyS):
        # Находит первое совпадение с желаемым элементом
        # В качестве желаемого принимает словарь из таких ключей, как NAME, COLOR, SIZE
        # anyS --- если нужен определенный размер - 0, если подойдет любой - 1
        elements = ""
        self.goTo(HOME + page)
        while True:
            try:
                elements = self.driver.find_elements_by_xpath("//div[@id='wrap']/div[@id='container']/article/div[@class='inner-article']/h1/a[@class='name-link']")
                break
            except exceptions.NoSuchElementException:
                continue
        for el in elements:
            if el.text == desirable["name"]:
                self.goTo(el.get_attribute('href'))
                if anyS:
                    self.getFirstItem()
                else:
                    sizes = self.driver.find_elements_by_tag_name("option")
                    self.getPerfectItem(sizes, desirable["size"])
                    self.goToCheckOut()
                return
