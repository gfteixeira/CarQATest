import sys
import time
import os.path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

global min_price
global max_price
global filename


def initFileText():
    if os.path.exists(filename):
        pass
    else:
        with open(filename, 'w') as txt_file:
            maxInt = sys.maxsize
            txt_file.write("min_price " + str(maxInt) + "\n")
            txt_file.write("max_price 0\n")


def readMinPrice():
    with open(filename, 'r') as txt_file:
        min_value = txt_file.readlines()
        min = min_value[0].split(" ")
        min_price = int(min[1])

    return min_price


def readMaxPrice():
    with open(filename, 'r') as txt_file:
        max_value = txt_file.readlines()
        max = max_value[1].split(" ")
        max_price = int(max[1])

    return max_price


def updateValue(arg, value):
    min = readMinPrice()

    max = readMaxPrice()
    with open(filename, 'w+') as txt_file:

        if arg == "min_price":
            txt_file.write(arg + " " + str(value) + "\n")
            txt_file.write("max_price " + str(max) + "\n")

        if arg == "max_price":
            txt_file.write("min_price " + str(min) + "\n")
            txt_file.write(arg + " " + str(value) + "\n")


def selectModel(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.maximize_window()
    time.sleep(5)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "uc-btn-accept-banner")))
    driver.find_element_by_id("uc-btn-accept-banner").click()

    iframe = driver.find_element_by_id('vmos-cont')
    driver.switch_to.frame(iframe)

    elem2 = driver.find_element_by_class_name("vmos_NvMoW")
    hover = ActionChains(driver).move_to_element(elem2)
    hover.perform()
    time.sleep(5)
    elem = driver.find_element_by_class_name("vmos_3HxTq.undefined")
    time.sleep(5)

    elem.click()
    time.sleep(5)


def carConfiguration(driver):
    driver.refresh()
    time.sleep(10)

    driver.execute_script("window.scrollTo(0, 972);")
    time.sleep(10)

    elem5 = driver.find_element_by_xpath("//input[@aria-labelledby='Diesel']")

    scroll = ActionChains(driver).move_to_element(elem5).click().perform()
    time.sleep(10)


def screenshots():
    driver.save_screenshot("cars_1.png")
    # #
    # # pagination = driver.find_elements_by_class_name(
    # #     "cc-motorization-comparision-status__pagination")
    #
    # buttonRq = driver.find_element_by_class_name("cc-slider-buttons__button--left.ng-star-inserted")
    #
    # #buttonR = driver.find_element_by_xpath("//button[@class='cc-slider-buttons__button--left.ng-star-inserted']")
    #
    # # buttonR = WebDriverWait(driver, 10).until(
    # #     EC.element_to_be_clickable((By.CLASS_NAME,
    # #                                 "cc-slider")))
    # print(buttonRq)
    # buttonRq.click()
    # driver.save_screenshot("cars_2.png")
    #
    # buttonRq.click()
    # driver.save_screenshot("cars_3.png")


def priceChecker():
    carsList = driver.find_elements_by_class_name(
        "cc-motorization-header__price.cc-text.ng-star-inserted")

    for car in carsList:
        driver.implicitly_wait(10)
        value = car.text.split('£')
        priceSplit = value[1].replace(',', '')
        price = int(priceSplit)
        min_price = readMinPrice()
        max_price = readMaxPrice()
        if price < min_price:
            updateValue('min_price', price)

        if price > max_price:
            updateValue('max_price', price)


def priceAssert():
    assert readMinPrice() >= 15000
    assert readMaxPrice() <= 60000


if __name__ == "__main__":

    filename = 'carPrice.txt'
    initFileText()

    try:
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        driver.get("http://www.mercedes-benz.co.uk")

        selectModel(driver)
        carConfiguration(driver)
        screenshots()
        priceChecker()
        priceAssert()


    finally:
        driver.close()
