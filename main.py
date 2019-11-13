from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
        #print(amt.value,serv.text)
     
class Plan:
    def _init_(self,cal=3000,meal=5):
        self.CAL = int(cal)
        self.MEALS = int(meal)
        if self.MEALS > 9:
            self.MEALS=9
        if self.MEALS < 1:
            self.MEALS = 1
        self.SITE = 'https://www.eatthismuch.com/'

    def doIt(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('chromedriver --log-level=OFF')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-logging")
        options.add_argument('log-level=3')
        driver = webdriver.Chrome(executable_path=r"C:\Users\user\Downloads\chromedriver.exe",options=options)
        driver.get(self.SITE)
        time.sleep(3)
        driver.find_element_by_id('cal_input').send_keys(self.CAL)
        meal = Select(driver.find_element_by_id('num_meals_selector'))
        meal.select_by_visible_text(str(self.MEALS)+' meals')
        driver.find_element_by_class_name('btn.btn-lg.btn-block.btn-orange.gen_button').click()
        time.sleep(5)
        #driver.find_element_by_xpath('//button[contains(text(), "GENERATE")]').click()
        titles = driver.find_elements_by_class_name('col.text-dark-gray.text-large.text-strong.print_meal_title.wrap_or_truncate.pr-0')
        #food_img = driver.find_elements_by_class_name('food_image')
        meals = driver.find_elements_by_class_name('meal_box.meal_container.row')
        for mel in meals:
            title = mel.find_element_by_class_name('col.text-dark-gray.text-large.text-strong.print_meal_title.wrap_or_truncate.pr-0')
            totCal = mel.find_element_by_class_name('cal_amount.text-small.text-light-gray')
            print()
            print(title.text)
            print('TOTAL CALORIES :',totCal.text)
            foods = mel.find_elements_by_class_name('diet_draggable.ui-sortable-handle')
            for food in foods:
                info = food.get_attribute('outerHTML')
                #print(info)
                img = food.find_element_by_class_name('food_image')
                lnk = img.get_attribute('style')
                #print(lnk)
                lnk = lnk[lnk.index('\"')+1:]
                #print(lnk)
                lnk = lnk[:lnk.index('\"')]
                #print("IMAGE",lnk)
                #print('\n\n')
                name = food.find_element_by_class_name('print_name')
                print(name.text)
                amt = food.find_element_by_class_name('amount_input')
                serv = food.find_element_by_class_name('food_units_selector')
                print()