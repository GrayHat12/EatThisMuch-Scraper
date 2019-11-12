from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

CAL = input("Calories : ")
MEALS = int(input("MEALS (1-9) : "))
if MEALS > 9:
    MEALS=9
if MEALS < 1:
    MEALS = 1
SITE = 'https://www.eatthismuch.com/'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=r"C:\Users\Rahul\PaidProjects\Personal\GrayBot-Uv1\chromedriver.exe",options=options)
driver.get(SITE)
time.sleep(3)
driver.find_element_by_id('cal_input').send_keys(CAL)
meal = Select(driver.find_element_by_id('num_meals_selector'))
meal.select_by_visible_text(str(MEALS)+' meals')
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
        print("IMAGE",lnk)
        #print('\n\n')
        name = food.find_element_by_class_name('print_name')
        print(name.text)
        amt = food.find_element_by_class_name('amount_input')
        serv = food.find_element_by_class_name('food_units_selector')
        print()
        #print(amt.value,serv.text)
        