import pandas as pd
import numpy as np 

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
        #print(amt.value,serv.text)
     
class Plan:
    def __init__(self,cal=3000,meal=5):
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
        driver = webdriver.Chrome(executable_path=r"C:\Users\Rahul\PaidProjects\Personal\GrayBot-Uv1\chromedriver.exe",options=options)
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

data=pd.read_csv("dataset.csv")

# male=0 and female=1 
data['Gender'].replace("Male",0,inplace=True)
data['Gender'].replace("Female",1,inplace=True)

# storing the feature matrix (X) and response vector (y) 
X = data[data.columns[:-1]] 
y = data[data.columns[-1]] 

#training testing and splitting the model data
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1) 

# training the model on training set 
from sklearn.neighbors import KNeighborsClassifier 
knn = KNeighborsClassifier(n_neighbors=3) 
knn.fit(X_train, y_train) 

# making predictions on the testing set 
y_pred = knn.predict(X_test) 
  
# comparing actual response values (y_test) with predicted response values (y_pred) 
from sklearn import metrics 
print("kNN model accuracy:", metrics.accuracy_score(y_test, y_pred)) 

ex=[]
print("Enter: ")
a=float(input("age: "))
g=input("gender: ")
if(g=='Male'or g=='male'):
	g=0
else:
	g=1
w=float(input("weight :"))
h=float(input("height: "))
ex.append([g,h,w])

ex=np.array(ex)
ex=ex.reshape(len(ex),-1)

prediction=knn.predict(ex)
print("Here Index :\n0 - Extremely Weak\n1 - Weak\n2 - Normal\n3 - Overweight\n4 - Obesity\n5 - Extreme Obesity")
print("Your index is : ",prediction[0])


import joblib 
joblib.dump(knn, 'diet.pkl')

#calorie requirement by Mifflin – St Jeor Formula

if g==0:
	 bmr=10*w+6.25*h-5*a+5
else:
	 bmr=10*w+6.25*h-5*a-161

print("Select the kind of lifestyle you lead : ")
print("1. Sedentry(little or no exercise)\n2. Lightly active (light exercise/sports 1-3 days/week)\n3. Moderately active (moderate exercise/sports 3-5 days/week)\n4. Very active (hard exercise/sports 6-7 days a week)\n5. Extra active (very hard exercise/sports & physical job or 2x training)\n")
op=int(input())

while True:
	if op==1:
		c=bmr*1.2
		break
	elif op==2:
		c=bmr*1.375
		break
	elif op==3:
		c=bmr*1.55
		break
	elif op==4:
		c=bmr*1.725
		break
	elif op==5:
		c=bmr*1.9
		break
	else:
		op=int(input("you entered wrong enter again: "))
print("Amount of calories you need to consume to maintain your current weight: ",c)


print("Do you want to :\n1. Lose weight\n2. Gain weight\n3. Maintain your present weight ")
op=int(input())
while True:
	if op==1:
		c=c-(0.2*c)
		break
	elif op==2:
		c=c+300
		break
	elif op==3:
		break
	else:
		op=input("you entered wrong enter again: ")
CAL = int(c)
MEALS = int(input("MEALS (1-9) : "))
ob=Plan(CAL,MEALS)
ob.doIt()