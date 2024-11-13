import requests
import time
import pandas as pd
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import re
import dataLoad



fileExcelLoad = pd.read_excel(f'{dataLoad.fileExcelLoad}', sheet_name="Sheet1")
linkCheck = f"http://{dataLoad.proxyLink}:6868/status?proxy={dataLoad.proxyLink}:"
linkReset = f"http://{dataLoad.proxyLink}:6868/reset?proxy={dataLoad.proxyLink}:"
linkGetip = f"http://{dataLoad.proxyLink}:6868/api/v1/proxy/public_ip?proxy={dataLoad.proxyLink}:"
linkresetAll = f"http://{dataLoad.proxyLink}:6868/reset_all"
linkFileip = dataLoad.fileIp
linkNoteAccFail = dataLoad.fileAccFail
linkNoteAccDie = dataLoad.fileAccDie
accPerTurn = int(dataLoad.accPerTurn)
fileSaveWalletKey = dataLoad.fileWalletKey
ref_group_link = dataLoad.ref_group_link
ref_url = dataLoad.ref_url
portProxyFrom = int(dataLoad.portProxyFrom)
api_url = "http://127.0.0.1:19995/api/v3/profiles/{action}/{id}"
time.sleep(1)
def run(x, i):
    setData1 = int(i)
    setData2 =int(x)
    portProxy1 = setData2 + portProxyFrom
    portProxy = str(portProxy1)
    linkCheckProxy = linkCheck + portProxy
    linkResetProxy = linkReset + portProxy
    linkGetipProxy = linkGetip + portProxy    
    rowProfile = setData1 + setData2
    tenProfile1 = fileExcelLoad.iloc[rowProfile, 0]
    tenProfile = str(tenProfile1)
    idTab1 = fileExcelLoad.iloc[rowProfile, 1]  
    profile_id = idTab1.strip()
    for openChrome in range(10):
        try:
            while True:
                checkIp = requests.get(linkCheckProxy)
                kqCheckip = checkIp.json()["status"]
                if kqCheckip:
                    print("PORT:", portProxy, "- Connected")
                    time.sleep(1)
                    while True:
                        getIpport = requests.get(linkGetipProxy)
                        ipPort = getIpport.json()["ip"]
                        with open(linkFileip, 'r') as fileip:
                            historyIp = fileip.read()
                            if ipPort not in historyIp:
                                print('Port', portProxy, "ip:", ipPort, 'GOOD !...')
                                with open(linkFileip, 'a+') as fileIpload:
                                    fileIpload.write(f'{ipPort}\n')
                                time.sleep(1)
                                break
                            else:
                                print('Port', portProxy, "ip:", ipPort, 'bị trùng lặp IP, đang reset lại ip !!!')
                                time.sleep(1)
                                requests.get(linkResetProxy)
                                time.sleep(20)
                            time.sleep(1)
                    time.sleep(1)
                    break
                else:
                    print("Port", portProxy, "Oẳng rồi, đang reset lại, đợi 15s !")
                    time.sleep(1)
                    requests.get(linkResetProxy)
                    time.sleep(20)
                time.sleep(1)
            time.sleep(1)
        except Exception as e:
            print("Error:", e)      
        time.sleep(1)    
        try:            
            line1 = x * 505
            line2 = (x-8)*505
            if x < 8:
                win_pos_value = f"{line1},5"
            else:
                win_pos_value = f"{line2},700"
            params = {
                "win_scale": 0.45,
                "win_pos": win_pos_value,
                "win_size": "500,700"
            }
            start_url = api_url.format(action="start", id=profile_id)
            response = requests.get(start_url, params=params)
            if response.status_code == 200:
                data = response.json()
                success_value = data.get('success')
                
                driver_path = data['data']['driver_path']
                remote_debugging_address = data['data']['remote_debugging_address']
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("debuggerAddress", remote_debugging_address)
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                try:
                    for tab in range(1,3):
                        driver.switch_to.window(driver.window_handles[tab])
                        driver.close()
                        time.sleep(0.3)
                except:time.sleep(0.5)
                print(f"Profile {tenProfile} mở thành công, code:{success_value}...Delay 6s before loading...")
                time.sleep(6)
                break
        except Exception as e:
            print(f"Đã có lỗi xảy ra: {tenProfile}>>>Đang quay lại từ đầu.")
            time.sleep(5)
            continue
    try:
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        driver.execute_script("window.open('chrome://settings/', '_blank');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0]) 
        for checkAcc in range(8):
            driver.get("chrome://settings/")
            time.sleep(1)
            try:        
                driver.get("https://web.telegram.org/k/")
                time.sleep(2)
            except:pass
            print(f'Đang check live acc telegram in profile {tenProfile}')
            if checkAcc == 7:
                print(f'{tenProfile}>>>Không check nổi..y học bó tay >>> close profile')
                time.sleep(1)
                close_url = api_url.format(action="close", id=profile_id)
                close_response = requests.get(close_url)
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
                    break
                else:
                    print("Lỗi khi đóng profile. Status code:", close_response.status_code)
            else:pass
            try:
                element = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.XPATH, '//h4[text()="Log in to Telegram by QR Code"]')))
                print(f'{tenProfile}>>>acc DIE cmnrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
                with open(linkNoteAccDie, 'a+') as noteAccDie:
                    noteAccDie.write(f'{tenProfile}|Die\n')
                time.sleep(1)
                close_url = api_url.format(action="close", id=profile_id)
                close_response = requests.get(close_url)
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
                    break
                else:
                    print("Lỗi khi đóng profile. Status code:", close_response.status_code)
            except:pass
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="input-search"][1]'))) 
                break
            except:pass
        print(f'{tenProfile} acc còn ngon zin >>> Vào Fang game...')
        for logGame in range(20):
            try:
                driver.get("chrome://settings/")
                time.sleep(1)
                driver.get(ref_group_link)
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="translatable-message"]//a[text()="{ref_url}"]')))
                driver.execute_script("arguments[0].click();", element)
            except:pass
            print(f'{tenProfile} Loading game...')
            try:
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Launch"]')))
                driver.execute_script("arguments[0].click();", element)
            except:pass
            try:
                iframe = WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="main-page-con"]/div[2]//div[@class="btn-next"]')))
                driver.execute_script("arguments[0].click();", element)
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="welcome-screen-con stay-tuned is-show"]//div[@class="btn-next"]')))
                driver.execute_script("arguments[0].click();", element)
            except:pass
            try:                
                element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="balance-wrap"]//div[text()="RANK"]')))
                break
            except:pass
        print(f"@{tenProfile}- Login game xong>>> Vào fang thoai")
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Connect wallet"]')))
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
            time.sleep(2)
            try:
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="View all"]')))
                driver.execute_script("arguments[0].click();", element)
            except:pass
            try:
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Telegram"]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
            except:pass
            try:
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Open Wallet in Telegram on desktop"]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
            except:pass
            time.sleep(2)
            driver.switch_to.default_content()
            time.sleep(1)
            try:
                element = WebDriverWait(driver, 18).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Connect"]'))) 
                print(f'@{tenProfile}>>đã có ví >>> connecting wl...')
            except:
                print(f'@{tenProfile} chwua có ví >>> vào reg ví...')
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="popup-container z-depth-1 have-checkbox"]//div[@class="checkbox-box"]')))
                    driver.execute_script("arguments[0].click();", element)
                    element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Continue"]')))
                    driver.execute_script("arguments[0].click();", element)
                except:pass
                try:
                    element = WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="popup-buttons"]//span[text()="Launch"]')))##
                    driver.execute_script("arguments[0].click();", element)
                except:pass

                iframe = WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//div[@style="background-color: rgb(255, 255, 255);"]//iframe[@class="payment-verification"]')))
                while True:
                    try:                        
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Start Exploring TON"]')))
                        driver.execute_script("arguments[0].click();", element)
                    except:pass
                    try:
                        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Back Up Manually"]')))
                        break
                    except:pass
                try:
                    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Back Up Manually"]')))
                    driver.execute_script("arguments[0].click();", element)
                except:pass
                keyBackup_list = []
                for keyText in range(1,25,1):
                    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="avlp"]/div[{keyText}]/div[2]')))
                    keyBackup = element.text
                    keyBackup_list.append(keyBackup)
                result_text = '|'.join(keyBackup_list)
                print(f'key {tenProfile}:::{result_text}')
                keybackup_acc = f"{tenProfile}:{result_text}\n"
                with open(fileSaveWalletKey, 'a+', encoding='utf-8') as file:
                    file.write(keybackup_acc)
                time.sleep(3)
                driver.switch_to.default_content()
                try:
                    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]')))
                    driver.execute_script("arguments[0].click();", element)
                except:pass
                key_to_fill_list = result_text.split('|')
                iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//div[@style="background-color: rgb(255, 255, 255);"]//iframe[@class="payment-verification"]')))
                element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@id="root"]/div[1]/div[3]')))
                banner_numberKey = element.text
                numbers = re.findall(r'\d+', banner_numberKey)
                number_key1 = int(numbers[0])
                trust_key1 = number_key1 - 1
                key_write1 = key_to_fill_list[trust_key1]
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//section[@class="DCcG _6Nch"]/button[1]//input[1]')))
                element.send_keys(key_write1)
                number_key2 = int(numbers[1])
                trust_key2 = number_key2 - 1
                key_write2 = key_to_fill_list[trust_key2]
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//section[@class="DCcG _6Nch"]/button[2]//input[1]')))
                element.send_keys(key_write2)
                number_key3 = int(numbers[2])
                trust_key3 = number_key3 - 1
                key_write3 = key_to_fill_list[trust_key3]
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//section[@class="DCcG _6Nch"]/button[3]//input[1]')))
                element.send_keys(key_write3)
                time.sleep(2)
                driver.switch_to.default_content()
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]')))
                driver.execute_script("arguments[0].click();", element)
                iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//div[@style="background-color: rgb(255, 255, 255);"]//iframe[@class="payment-verification"]')))
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="View TON Space"]')))
                driver.execute_script("arguments[0].click();", element)
                time.sleep(4)
                driver.switch_to.default_content()
            time.sleep(1)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Connect"]')))
            driver.execute_script("arguments[0].click();", element)
            time.sleep(10)
            print(f"{tenProfile}>>>>>>>>connect xong wl>>>vào fang task")
        except:print(f"{tenProfile}>>>>>>>>Đã connect wl >>> vào fang task")
        for logGame in range(6):
            try:
                driver.get("chrome://settings/")
                time.sleep(1)
                driver.get(ref_group_link)
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="translatable-message"]//a[text()="{ref_url}"]')))
                driver.execute_script("arguments[0].click();", element)
            except:pass
            print(f'{tenProfile} Loading game...')
            try:
                element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Launch"]')))
                driver.execute_script("arguments[0].click();", element)
            except:pass
            try:
                iframe = WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="main-page-con"]/div[2]//div[@class="btn-next"]')))
                driver.execute_script("arguments[0].click();", element)
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="welcome-screen-con stay-tuned is-show"]//div[@class="btn-next"]')))
                driver.execute_script("arguments[0].click();", element)
            except:pass
            try:                
                element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="balance-wrap"]//div[text()="RANK"]')))
                break
            except:pass
        ###//////////////////////////////////////////////////////////////////
        print(f'@{tenProfile}> Fang task ...')
        for logTaskFang in range(6):
            try:
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="nav-bar-con"]/div[4]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
                time.sleep(2)
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="nav-bar-con"]/div[5]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
            except:pass
            try:                
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="heading-con"]//div[text()="Tasks"]')))
                
                break
            except:pass
            time.sleep(1)
        for doTask in range(1,3,1):
            if doTask == 2:
                element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="type-select"]//div[text()="Partners"]')))
                driver.execute_script("arguments[0].click();", element)                
                try:
                    for c1Start in range(1,5,1):
                        print(f'@{tenProfile}> Đang Click <START> lần {c1Start}')
                        element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="section-items-con quests"]//div[text()="Start"][1]')))
                        driver.execute_script("arguments[0].click();", element)                 
                        try:
                            for tab in range(2,5,1):
                                driver.switch_to.window(driver.window_handles[tab])
                                driver.close()
                                time.sleep(0.3)
                        except:time.sleep(0.5)
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get("chrome://settings/")
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[0])
                        iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                except:pass
            elif doTask == 1:
                element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="type-select"]//div[text()="In-game"]')))
                driver.execute_script("arguments[0].click();", element)
                for c2Start in range(1,7,1):
                    c2Start_string = str(c2Start)
                    xpath_start = f'//div[@class="section-items-con quests"]/div[{c2Start_string}]//div[text()="Start"][1]'
                    try:
                        print(f'@{tenProfile}> Đang Click <START> lần {c2Start}')
                        if c2Start == 3:
                            pass
                        elif c2Start == 5:
                            pass
                        else:
                            element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, xpath_start)))
                            driver.execute_script("arguments[0].click();", element)                  
                            try:
                                for tab in range(2,5,1):
                                    driver.switch_to.window(driver.window_handles[tab])
                                    driver.close()
                                    time.sleep(0.3)
                            except:time.sleep(0.5)
                            driver.switch_to.window(driver.window_handles[1])
                            driver.get("chrome://settings/")
                            time.sleep(2)
                            driver.switch_to.window(driver.window_handles[0])
                            iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                    except:print(f'+++>Hết <START> tabTask{doTask} in: {tenProfile}')
                
                for c1Check in range(1,7,1):
                    c1Check_string = str(c1Check)
                    xpath_check = f'//div[@class="section-items-con quests"]/div[{c1Check_string}]//div[text()="Check"][1]'
                    print(f'@{tenProfile}> Đang Click <CHECK> lần {c1Check}')
                    if c1Check == 3 :pass
                    elif c1Check == 5 :pass
                    else:
                        try:                    
                            element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH,xpath_check )))
                            driver.execute_script("arguments[0].click();", element)
                        except:pass
                        randomWait = random.randint(11,19)
                        waitTime = randomWait/10
                        time.sleep(waitTime)
                
            else:pass
            try:
                for c1Claim in range(1,11,1):                    
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Claim"][1]')))
                    driver.execute_script("arguments[0].click();", element)
                    print(f'{tenProfile} clicked <claim> turn {c1Claim}')
                    randomWait1 = random.randint(35,49)
                    waitTime1 = randomWait1/10
                    time.sleep(waitTime1)
            except:print(f'+++>Hết <CLAIM> tabTask{doTask} in: {tenProfile}')     
        print(f'>>>>>> <DONE> : {tenProfile}>>>>Profile will close in 3s...')
        time.sleep(2)
    except Exception as e:
        print(f"Acc {tenProfile} FAIL-saving info to file note !!!! Error: {str(e)}")
        with open(linkNoteAccFail, 'a+') as noteAccFail:
            noteAccFail.write(f'{tenProfile}|{profile_id}|error #Fang Paw\n')
        time.sleep(1)
        close_url = api_url.format(action="close", id=profile_id)
        close_response = requests.get(close_url)
        if close_response.status_code == 200:
            close_data = close_response.json()
            print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
        else:
            print("Lỗi khi đóng profile. Status code:", close_response.status_code)
    finally:
        try:
            close_url = api_url.format(action="close", id=profile_id)
            close_response = requests.get(close_url)
            if close_response.status_code == 200:
                close_data = close_response.json()
                print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
            else:
                print("Lỗi khi đóng profile. Status code:", close_response.status_code)
        except:pass
try:
    for i in range(0, 5000, accPerTurn):
        
        idBeginturnacc = str(fileExcelLoad.iloc[i, 1])
        print(f"Turn bắt đầu từ acc: {fileExcelLoad.iloc[i, 0]}")
        if len(idBeginturnacc) < 10:
            break

        threads = []
        for x in range(accPerTurn):
            t = threading.Thread(target=run, args=(x, i))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print(">>ĐÃ QUẤT XONG TURN ACC !!!")
        print("Đang reset ip để chạy turn tiếp")
        time.sleep(1)
        requests.get(linkresetAll)
        print("")
        print("----Reset IP thành công, Vui lòng đợi 20s !------")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for fap69 in range(18,0,-1):
            print(f'Continue in {fap69}s !')
            time.sleep(1)
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    print("*************************************************")
    print("-------------ĐÃ QUẤT XONG LÔ ACC ----------------")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


