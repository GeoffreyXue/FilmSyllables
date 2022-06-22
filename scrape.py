from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
  
# Create webdriver object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Get the website
driver.get(r"https://imsdb.com/scripts/Social-Network,-The.html")
  
# Make Python sleep for some time
sleep(3)

# with open("./test.html", "w", encoding="utf-8") as f:
#     f.write(driver.page_source)

# drills to script, written in innerHTML and b
script_html = driver.find_element(By.TAG_NAME, 'pre')

with open("./test.txt", "w", encoding="utf-8") as f:
    f.write(script_html.get_attribute('innerHTML'))
  
# # Obtain the number of rows in body
# rows = 1+len(driver.find_elements_by_xpath(
#     "/html/body/div[3]/div[2]/div/div[1]/div/div/div/article/div[3]/div/table/tbody/tr"))
  
# # Obtain the number of columns in table
# cols = len(driver.find_elements_by_xpath(
#     "/html/body/div[3]/div[2]/div/div[1]/div/div/div/article/div[3]/div/table/tbody/tr[1]/td"))
  
# # Print rows and columns
# print(rows)
# print(cols)
  
# # Printing the table headers
# print("Locators           "+"             Description")
  
# # Printing the data of the table
# for r in range(2, rows+1):
#     for p in range(1, cols+1):
        
#         # obtaining the text from each column of the table
#         value = driver.find_element_by_xpath(
#             "/html/body/div[3]/div[2]/div/div[1]/div/div/div/article/div[3]/div/table/tbody/tr["+str(r)+"]/td["+str(p)+"]").text
#         print(value, end='       ')
#     print()