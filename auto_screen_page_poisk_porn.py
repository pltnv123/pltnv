
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome("C:\dev\chromedriver.exe")
driver.get("http://130.193.37.179/app/pets")
# driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
t = (driver.find_element(By.XPATH, "//*[@id=\"image\"]/img")).click()
# driver.find_element(By.XPATH, "//input[@title=\'Поиск\']").send_keys('Porn' + Keys.RETURN)
print(t)
sleep(2)
# driver.save_screenshot('sf.png')
driver.quit()