import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv


load_dotenv()
get_member_num=os.environ.get("member_num")
get_pw=os.environ.get("pwd")
get_depart_station=os.environ.get("depart_station")
get_arrival_station=os.environ.get("arrival_station")
get_depart_date=os.environ.get("depart_date")
get_depart_time=os.environ.get("depart_time")

driver=webdriver.Chrome("chromedriver")

driver=webdriver.Chrome("chromedriver")
driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
driver.implicitly_wait(15)

driver.find_element(By.ID, 'srchDvNm01').send_keys(get_member_num)
driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(get_pw)
driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
driver.implicitly_wait(5)

driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
driver.implicitly_wait(5)

dep_stn=driver.find_element(By.ID, 'dptRsStnCdNm')
dep_stn.clear()
dep_stn.send_keys(get_depart_station)

arr_stn=driver.find_element(By.ID, 'arvRsStnCdNm')
arr_stn.clear()
arr_stn.send_keys(get_arrival_station)

elm_dptDt=driver.find_element(By.ID, "dptDt")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)

Select(driver.find_element(By.ID,"dptDt")).select_by_value(get_depart_date)

elm_dptTm=driver.find_element(By.ID, "dptDt")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(get_depart_time)

driver.find_element(By.XPATH,"//input[@value='조회하기']").click()

train_list=driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr')

#print(len(train_list))

# for i in range(1, (get_number_of_trains + 1)):
#     for j in range(3, 8):
#         text=driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({j})").text.replace("\n", " ")
#         print(text, end="")
#     print()

is_booked=False
want_reserve=False
is_not_booked_count=0
while True:
    for i in range(1, 5):
        standard_seat=driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
        reservation = driver.find_element(By.CSS_SELECTOR,
                                            f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text
        if "예약하기" in standard_seat:
            print("예약 가능")
            driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a").click()
            driver.implicitly_wait(2)

            if driver.find_elements(By.ID, 'isFalseGotoMain'):
                is_booked=True
                print("예약 성공")
                break

            else:
                print("잔여석 없음. 다시 검색")
                driver.back()
                driver.implicitly_wait(2)
        if want_reserve:
            if "신청하기" in reservation:
                print("예약 대기 완료")
                driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8) > a").click()
                is_booked=True
                break

    if not is_booked:
        time.sleep(2)

        submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
        driver.execute_script("arguments[0].click();", submit)
        is_not_booked_count+=1

        print("새로고침 ", is_not_booked_count, "회")
        driver.implicitly_wait(2)
        time.sleep(0.5)

    else:
        break
