
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from cryptography.fernet import Fernet
import configuration
import requests
import time
import yaml
import re
import os



class End2EndTester():
    def __init__(self,headless) :
        if headless : 
            # options = Options()
            # options.add_argument("--headless=new")
            # self.driver = webdriver.Chrome(options=options)
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            #self.driver = webdriver.Chrome(options=options)
            self.driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',  # Adresse du serveur Selenium
    options=options
)
        else : 
            self.driver = webdriver.Chrome()
        
        #self.driver.maximize_window()
        self.action = ActionChains(self.driver)
        
        # options = webdriver.EdgeOptions()
        # driver = webdriver.Edge(options=options)
        self.load_configuration()

    def load_configuration(self):

        self.ROBOT_INFORMATION_BUTTON = configuration.robot_information_button
        self.SIDE_BAR_BUTTON = configuration.side_bar_button
        self.SITE_ELEMENT = configuration.site_element
        self.SITE_NAME = configuration.site_name
        self.SIDE_BAR_NAVIGATION = configuration.side_bar_navigation
        self.LOGO_DASHBOARD_UAVIA =configuration.logo_dashboard_uavia
        self.ROBOT_FLY_BUTTON = configuration.robot_fly_button
        self.DIALOG_MISSION_TITLE = configuration.dialog_mission_title
        self.ROBOT_START_BUTTON = configuration.robot_start_button
        self.TAKE_OFF_BUTTON = configuration.take_off_button
        self.ACTIVITY_LABEL = configuration.activity_label 
        self.BATTERY_INDICATION = configuration.battery_indication

        self.FLIGHT_PLAN_SECTION_TO_OPEN = configuration.flight_plan_section_to_open
        self.FLIGHT_PLAN_SECTION_TO_CLOSE = configuration.flight_plan_section_to_close 
        self.SLIDER_ALTITUDE = configuration.slider_altitude 
        self.SLIDER_LABEL_ALTITUDE = configuration.slider_label_altitude
        self.SLIDER_SPEED = configuration.slider_speed 
        self.SLIDER_LABEL_SPEED = configuration.slider_label_speed
        self.RETURN_HOME_BUTTON = configuration.return_home_button
        self.STOP_RED_BUTTON = configuration.stop_red_button
        self.STOP_MISSION_BUTTON = configuration.stop_mission_button
        self.INFO_ELEMENT = configuration.info_element
        self.MISSION_TIME = configuration.mission_time 
        self.NOTIF_BUTTON = configuration.notif_button 
        self.PARTICIPANT_BUTTON = configuration.participant_button 
        self.SENSOR_BUTTON = configuration.sensor_button

    def gotoDashbaordPageFN(self):
        print("--------- RETRUN TO DASHBOARD ------------")
        logo_click_dashboard = self.driver.find_elements(By.XPATH, self.LOGO_DASHBOARD_UAVIA) 
        logo_click_dashboard[0].click()
        print("--------- ------------------- ------------")

    def sidebarNavigationFN(self):
        # Side Bar Navigation : 
        side_bar_button = self.driver.find_elements(By.XPATH, self.SIDE_BAR_NAVIGATION) 
        print(f"SIDE BAR : {len(side_bar_button)} button in side bar")

        for element in side_bar_button :
            print(f"----- CLICK on side bar element  -------")
            element.click()
            print("-------- CLICKED ---------")
            time.sleep(1)
            self.gotoDashbaordPageFN()
            time.sleep(1)

    def siteNameVerificationFN(self,site_name):
        title_site = self.driver.find_elements(By.XPATH, self.SITE_NAME) 
        title_site = title_site[0].text
        if title_site == site_name :
            print("CORRECT SITE")
        else : 
            print("WRONG SITE --> SWAPING SITE ...")
            self.swapSiteFN(site_name=site_name)
        

    def swapSiteFN(self,site_name):
        print("--------- Ouverture side tab -----------")
        button_site_bar = self.driver.find_elements(By.XPATH, self.SIDE_BAR_BUTTON)
        button_site_bar[0].click()
        time.sleep(1)
        list_of_sites = self.driver.find_elements(By.XPATH, self.SITE_ELEMENT) 
        i = 0 
        while i < len(list_of_sites) : 
            if list_of_sites[i].text == site_name :
                print(f"element {i} : {list_of_sites[i].text}")
                list_of_sites[i].click()
                time.sleep(1)
                break
            else : 
                i = i + 1

    def sideTabVerificationFN(self):
        print("--------- Ouverture side tab -----------")
        button_site_bar = self.driver.find_elements(By.XPATH, self.SIDE_BAR_BUTTON)
        button_site_bar[0].click()
        time.sleep(1)
        list_of_sites = self.driver.find_elements(By.XPATH, self.SITE_ELEMENT) 
        print(f"Nombre de site disponible = {len(list_of_sites)}")
        if len(list_of_sites) > 1:
            for i in range(len(list_of_sites)):
                try : 
                    print(f"element {i} : {list_of_sites[i].text}")
                except :
                    print("not a text")
        time.sleep(2)
        print("--------- Fermeture side tab -----------")
        button_site_bar[0].click()

    def robotInfoPageVerification(self):
        list_of_button_info_robot = self.driver.find_elements(By.XPATH, self.ROBOT_INFORMATION_BUTTON)

        # Go to robot information page
        for specific_button_index in range(len(list_of_button_info_robot)):
            print("------ GO to ROBOT PAGE --------")
            list_of_button_info_robot = self.driver.find_elements(By.XPATH, self.ROBOT_INFORMATION_BUTTON)
            # click on robot information 
            print(len(list_of_button_info_robot))
            list_of_button_info_robot[specific_button_index].click()
            robot_name = self.driver.find_elements(By.CLASS_NAME, 'title-page')
            print(f'ROBOT : {robot_name[0].text}')
            self.getRobotInformationDetailsFN()
            time.sleep(1)
            #TODO wait for robot information not sleep method
            print("------ EXIT ROBOT PAGE --------")
            self.gotoDashbaordPageFN()
            time.sleep(1)

    def getRobotInformationDetailsFN(self):
        print("----- getRobotInformationDetailsFN ------")
        info_element = self.driver.find_element(By.XPATH, self.INFO_ELEMENT)
        robot_info = info_element.text.split('\n')
        print(f"{robot_info[0]} : {robot_info[1]}")
        print(f"{robot_info[2]} : {robot_info[3]}")
        print(f"{robot_info[4]} : {robot_info[5]}")
        print(f"{robot_info[6]} : {robot_info[7]}")
        print("----- ---------------------------- ------")


    def readConfig(self,env):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(config_dir, "config.yml")
        with open(config_path, 'r') as file:
            config_file = yaml.safe_load(file)

        URP_app_link = config_file['URP-'+env]['url']

        return (URP_app_link,self.decryptLogInInfo(dir=config_dir,config_file=config_file))

    def decryptLogInInfo(self,dir,config_file):
        print("------ LOGIN TO URP --------")
        key_path = os.path.join(dir, "logInURP.key")

        with open(key_path, 'rb') as key_file:
            key = key_file.read()

        cipher_suite = Fernet(key)

        encrypted_password = config_file['password']
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()

        print("Login:", config_file['username'])
        print("Successfully Encryped password KEY")

        return (config_file['username'],decrypted_password)


    def LoginFN(self,userInfo):
        # LOG IN PAGE
        self.driver.find_element(By.NAME, "email").send_keys(userInfo[0], Keys.ARROW_DOWN)
        self.driver.find_element(By.NAME, "password").send_keys(userInfo[1], Keys.ARROW_DOWN)
        self.driver.find_element(By.XPATH, '//*[@id="account-panel"]/app-login-view/form/button').click()
        print("------ ------------ --------")

    def verifyTitleWebFN(self,title_page):
        assert title_page in self.driver.title

    def goToWebPage(self,url_link):
        self.driver.get(url_link)


    def verifyRobotNameMissionFN(self,name):
        dialog_title = self.driver.find_elements(By.XPATH,self.DIALOG_MISSION_TITLE)

        # dialog_title_splited = dialog_title[0].text.split('\n')
        # robot_name_mixed = dialog_title_splited[0].split("-")
        # robot_name = robot_name_mixed[1:][1:]

        dialog_title_splited = dialog_title[0].text.split('\n')
        robot_name_mixed = dialog_title_splited[0].split("-")
        robot_name = '-'.join(robot_name_mixed[1:]).replace(" ","")

        if robot_name == name : 
            print(f"robot name = {robot_name} is the CORRECT robot choosen")
            return True
        else : 
            print(f"robot name = {robot_name} is the WRONG robot")
            return False

    def get_list_of_button_fly_nowFN(self,index):
        try :
            list_of_button_fly_now_robot = self.driver.find_elements(By.XPATH, self.ROBOT_FLY_BUTTON) 
            list_of_button_fly_now_robot[index].click()
            print("GET IT NO REFRESH PB ;)")
            return True
        except IndexError:
            print(f"(WARNING REFRESH) ERROR: Index {index} is out of range for the list of buttons.")
            return False
        
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"WARNING REFRESH PB ;) - {str(e)}")
            return False
        
        except Exception as e:
            print(f"WARNING REFRESH Unexpected error: {str(e)}")
            return False

    def launchMissionRobotFN(self,name):
        specific_button_index = 0
        list_of_button_fly_now_robot = self.driver.find_elements(By.XPATH, self.ROBOT_FLY_BUTTON) 
        print(f"Nombre de button flynow robot = {len(list_of_button_fly_now_robot)}")
        if len(list_of_button_fly_now_robot) > 1:
            print("SEARCHING FOR THE ROBOT ... ")        
            flag_while = True
            while flag_while and (specific_button_index < len(list_of_button_fly_now_robot)): 
                print(f"specific_button_index = {specific_button_index}")
                no_refresh_list_pb = False
                while not(no_refresh_list_pb) :
                    no_refresh_list_pb = self.get_list_of_button_fly_nowFN(index=specific_button_index)
                time.sleep(1)
                robot_name_status = self.verifyRobotNameMissionFN(name=name)
                if not(robot_name_status) : 
                    print("CANCEL ")
                    cancel_button = self.driver.find_elements(By.XPATH, '//div[contains(@class, "mdc-dialog__container")]//button[contains(@class, "btn-cancel")]') 
                    cancel_button[0].click()
                    specific_button_index = specific_button_index + 1
                    time.sleep(0.2)
                else : 
                    print("ROBOT FOUND :) ")
                    flag_while = False
                    time.sleep(1)
                    start_button = self.driver.find_elements(By.XPATH, self.ROBOT_START_BUTTON) 
                    start_button[0].click()
                    time.sleep(10) # wait to enter cockpit (i should find a way to wait dynamically)
                    return True
                
        print("ROBOT NOT FOUND :( ")
        return False
            

    def footerInfoFN(self):
        print("----- COCKPIT INFORMATION TOP/BOTTOM BAR --------")
        # get info mission time : 
        mission_time = self.driver.find_element(By.XPATH, self.MISSION_TIME)
        print(f"TIME : {mission_time.text}")

        # get notif button
        time.sleep(0.5)
        notif_button = self.driver.find_element(By.XPATH,self.NOTIF_BUTTON)
        notif_button.click()
        time.sleep(0.5)
        notif_button.click()

        # get participant button
        time.sleep(0.5)
        participant_button = self.driver.find_element(By.XPATH, self.PARTICIPANT_BUTTON)
        participant_button.click()
        time.sleep(0.5)
        participant_button.click()

        # get sensor button
        time.sleep(0.5)
        sensor_button = self.driver.find_element(By.XPATH,self.SENSOR_BUTTON)
        sensor_button.click()
        time.sleep(0.5)
        sensor_button.click()

        # get activity status
        activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        print(f"ROBOT ACTIVITY = {activity_label.text}")

        # get battery status
        battery_div = self.driver.find_element(By.XPATH, self.BATTERY_INDICATION)

        style_value = battery_div.get_attribute("style")

        width_match = re.search(r"width:\s*([\d.]+)%", style_value)
        if width_match:
            battery_width = float(width_match.group(1))
            print(f"Niveau de charge de la batterie : {battery_width}%")
                    
            # Vérifiez si le niveau de charge est suffisant
            if battery_width > 50:
                print("--> Le niveau de batterie est suffisant")
            else:
                print("--> La batterie est faible. inferieur à 50 % ")
        else:
            print("**** Impossible de déterminer le niveau de charge ****")

        print("----- ---------------------------------- --------")

    def actionMissionFN(self,robot_simu,id):
        
        # COCKPIT INFORMATION 
        #self.footerInfoFN()

        # SET ALTITUDE
        #self.setAltitudeSliderFN(altitude_goal=20)
        #time.sleep(1)

        # SET SPEED
        #self.setSpeedSliderFN(speed_goal=20)
        #time.sleep(1)

        # TAKE OFF
        #self.takingOffFN(robot_simu,takeoff_altitude=20)
        self.get_coockies()
        self.take_off_api(id,altitude=30)
        time.sleep(1)

        # TAKE OFF
        #self.takingOffFN(robot_simu,takeoff_altitude=20)
        #self.go_to_api(altitude=40)
        self.loop_go_to_api(id,altitude=40)

        time.sleep(1)

        # RETURN HOME
        #self.returnHomeFN()
        self.go_home_api(id)

        # STOP MISSION
        self.stopMissionFN()
        time.sleep(2)

        # MISSION INFOS
        self.missionInfoPage()

        time.sleep(10)

    def loop_action(self,robot_simu,id):
        while True:
            # TAKE OFF
            self.get_coockies()
            self.take_off_api(id,altitude=30)
            #self.loop_go_to_api(id,altitude=40)
            self.go_to_api(id,altitude=30)
            time.sleep(1)

            # RETURN HOME
            self.returnHomeFN()
            time.sleep(2)
            reponse_util = input("Je continue ?? ")
            if reponse_util == "no":
                return


    def missionInfoPage(self): # ON DEV ...
        print("----- MISSON INFORMATION ------")
        mission_card_infos = self.driver.find_element(By.XPATH, '//div[contains(@id, "content")]//div[contains(@class, "page-row")]//mat-card[contains(@class, "mat-mdc-card")]//div[contains(@class, "card-title")]')
        
        print(f"title of mission card = {mission_card_infos.text}")
        robot_card_infos = self.driver.find_element(By.XPATH, 
                                                '//div[contains(@id, "content")]//div[contains(@class, "page-row")]\
                                                //mat-card[contains(@class, "mat-mdc-card")]\
                                                //div[contains(@class, "robot-info")]')
        robot_card_infos = robot_card_infos.text.split('\n')
        print(f"ROBOT NAME (MISSION) = {robot_card_infos[0]}","| Payload : ",robot_card_infos[1])

        parent_div = self.driver.find_element(By.XPATH,'//div[contains(@class, "info-mission-subsection")]')
        children = parent_div.find_elements(By.XPATH, './*')

        for child in children:
            info = child.text.split('\n')
            print(info[0], info[1])

        print("----- ------------------ ------")

        # card title (Flight Map)
    
    def openFlightPlanFN(self):
        flight_plan_section = self.driver.find_element(By.XPATH, self.FLIGHT_PLAN_SECTION_TO_OPEN)
        print("-- Ouverture section flight plan --")
        flight_plan_section.click()
        time.sleep(2)
        flight_plan_section = self.driver.find_element(By.XPATH, self.FLIGHT_PLAN_SECTION_TO_CLOSE)
        print("-- Fermeture section flight plan --")
        flight_plan_section.click()


    def setAltitudeSliderFN(self,altitude_goal):
        # Localisez le curseur du slider altitude 
        slider_altitude = self.driver.find_element(By.XPATH, self.SLIDER_ALTITUDE)
        slider_label_altitude = self.driver.find_element(By.XPATH, self.SLIDER_LABEL_ALTITUDE)
        print ('---- SET ALTITUDE ----')
        print(f"ALTITUDE = {slider_label_altitude.text}")

        # Récupérer la valeur actuelle
        current_value = int(slider_altitude.get_attribute("aria-valuenow"))
        print(f"Valeur actuelle du slider : {current_value}")

        # Définir le déplacement nécessaire pour atteindre une nouvelle valeur
        slider_max = int(slider_altitude.get_attribute("aria-valuemax"))
        slider_min = int(slider_altitude.get_attribute("aria-valuemin"))
        slider_height = slider_altitude.size['height']  # Hauteur du slider en pixels

        print(f"slider_max = {slider_max}, slider_min = {slider_min}, slider_height = {slider_height}")

        # Calculer le déplacement vertical en pixels
        pixels_to_move = int(((altitude_goal - current_value) / (slider_max - slider_min)) * slider_height)
        print(f"pixels_to_move in float  = {(((altitude_goal - current_value) / (slider_max - slider_min)) * slider_height)}")
        print(f"pixels_to_move = {pixels_to_move}")
        
        # Effectuer le déplacement
        self.action.click_and_hold(slider_altitude).move_by_offset(0, -pixels_to_move).release().perform()

        # Vérifier la nouvelle valeur
        new_value = int(slider_altitude.get_attribute("aria-valuenow"))
        print(f"Nouvelle valeur du slider : {new_value}")
        print ('---- ------------ ----')
    
    def setSpeedSliderFN(self,speed_goal):
        # Localisez le curseur du slider speed 
        slider_speed = self.driver.find_element(By.XPATH, self.SLIDER_SPEED)
        slider_label_speed = self.driver.find_element(By.XPATH, self.SLIDER_LABEL_SPEED)
        print ('---- SET SPEED ----')
        print(f"SPEED = {slider_label_speed.text}")
    
        # Récupérer la valeur actuelle
        current_value = int(slider_speed.get_attribute("aria-valuenow"))
        print(f"Valeur actuelle du slider : {current_value}")

        # Définir le déplacement nécessaire pour atteindre une nouvelle valeur
        slider_max = int(slider_speed.get_attribute("aria-valuemax"))
        slider_min = int(slider_speed.get_attribute("aria-valuemin"))
        slider_height = 190 #slider_speed.size['height']  # Hauteur du slider en pixels

        print(f"slider_max = {slider_max}, slider_min = {slider_min}, slider_height = {slider_height}")

        # Calculer le déplacement vertical en pixels
        pixels_to_move = int(((speed_goal - current_value) / (slider_max - slider_min)) * slider_height)
        print(f"pixels_to_move in float  = {(((speed_goal - current_value) / (slider_max - slider_min)) * slider_height)}")
        print(f"pixels_to_move = {pixels_to_move}")

        # Effectuer le déplacement
        self.action.click_and_hold(slider_speed).move_by_offset(0, -pixels_to_move).release().perform()

        # Vérifier la nouvelle valeur
        new_value = int(slider_speed.get_attribute("aria-valuenow"))
        print(f"Nouvelle valeur du slider : {new_value}")
        print ('---- --------- ----')
    
    def returnHomeFN(self):
        print('---- RETUNRNING HOME ------')
        return_home_button = self.driver.find_element(By.XPATH, self.RETURN_HOME_BUTTON)
        return_home_button.click()
        time.sleep(0.5)

        activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        print(activity_label.text)

        print("WAIT FOR END OF RTH ...")
        while activity_label.text != "GROUNDED" : 
            time.sleep(0.5)
            activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        
        print("End of RTH --> ready for next actions")
        time.sleep(1)
        print('---- --------------- ------')

    def takingOffFN(self,robot_simu,takeoff_altitude):
        print("----- TAKE OFF ------")
        #self.setAltitudeSliderFN(altitude_goal=takeoff_altitude)
        time.sleep(1)

        takeoff_button = self.driver.find_elements(By.XPATH, self.TAKE_OFF_BUTTON) 
        self.action.click_and_hold(takeoff_button[0]).pause(3).release().perform() 
        time.sleep(1)

        activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        print(activity_label.text)

        if not robot_simu : 
        # confirmation 
            takeoff_button_confirmation = self.driver.find_elements(By.XPATH,'//div[contains(@class, "mdc-dialog__container")]//button[contains(@class, "btn-orange")]') 
            print(f"takeoff_button_confirmation : {takeoff_button_confirmation}")
            takeoff_button_confirmation[0].click()
            time.sleep(1)
        print("WAIT FOR END OF TAKE OFF ... ")
        while activity_label.text != "FLYING" : 
            time.sleep(0.5)
            activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        
        print("End of take off --> ready for next actions")
        time.sleep(1)
        print("----- -------- ------")

    def stopMissionFN(self):
        print("----- STOPPING MISSION ------")
        stop_red_button = self.driver.find_element(By.XPATH, self.STOP_RED_BUTTON)
        stop_red_button.click()
        time.sleep(1)
        stop_mission_button = self.driver.find_element(By.XPATH, self.STOP_MISSION_BUTTON)
        stop_mission_button.click()
        print("----- --------------- ------")

    def get_coockies(self):
        selenium_cookies = self.driver.get_cookies()
        # Transformer les cookies en format compatible avec requests
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

        self.chrome_session = requests.Session()
        self.chrome_session.cookies.update(cookies)

    def go_home_api(self,id):
        url_land = f"https://app.uavia.eu/robotscontrolwebservice/api/{id}/navigation/go/home"
        response = self.chrome_session.put(url_land)

        print(f"go_home_api : ",response.status_code)
        activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        print("WAIT FOR END OF RTH ...")
        while activity_label.text != "GROUNDED" : 
            time.sleep(0.5)
            activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        
        print("End of RTH --> ready for next actions")
        time.sleep(1)
        print('---- --------------- ------')
    
    def take_off_api(self,id,altitude):
        url_take_off = f"https://app.uavia.eu/robotscontrolwebservice/api/{id}/navigation/takeOff"
        body_data = {
            "altitude": altitude
        }
        response = self.chrome_session.post(url_take_off,json=body_data)

        print(f"take_off_api : ",response.status_code)
        activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        print("WAIT FOR END OF TAKE OFF ... ")
        while activity_label.text != "FLYING" : 
            time.sleep(0.5)
            activity_label = self.driver.find_element(By.XPATH, self.ACTIVITY_LABEL)
        
        print("End of take off --> ready for next actions")
        time.sleep(1)
        print("----- -------- ------")

    def go_to_api(self,id,altitude):
        url_go_to = f"https://app.uavia.eu/robotscontrolwebservice/api/{id}/navigation/go"
        #goto simu#48.590628434166376,2.3269074429577756
        go_to_target = {
        "lat": 48.590835545281635,
        "lng": 2.3366662736470403,
        "alt": altitude,
        "isRelativeAltitude": True,
        "strategy": "GOTO_STRATEGY_NONE"
        }
        #48.59057521096702, 2.326182246524553
        #48.59013168212644, 2.3258281949349566
        #48.58983717682543, 2.3264504674257296
        response = self.chrome_session.put(url_go_to,json=go_to_target)

        print(f"go_to_api : ",response.status_code)

        time.sleep(3)

    def poi_api(self,id):
        url_poi = f"https://app.uavia.eu/robotscontrolwebservice/api/{id}/navigation/roi/location"
        poi_target = {
        "lat": 48.59057521096702,
        "lng": 2.326182246524553,
        "alt": 0,
        "isRelativeAltitude": True
        }
        response = self.chrome_session.put(url_poi,json=poi_target)

        print(f"poi_api : ",response.status_code)

        time.sleep(3)

    def delete_poi_api(self,id):
        url_delete_poi = f"https://app.uavia.eu/robotscontrolwebservice/api/{id}/navigation/roi"
        response = self.chrome_session.delete(url_delete_poi)
        print(f"delete_poi_api : ",response.status_code)


    def loop_go_to_api(self,id,altitude):
        self.poi_api(id=id)
        time.sleep(1)
        
        #go_list = [(48.59057521096702,2.326182246524553),(48.59013168212644, 2.3258281949349566),(48.58983717682543, 2.3264504674257296)]
        go_list_zone2_bretigny = [(48.59089862725142,2.3363266932436204),(48.59080406448609, 2.336680347965512),(48.590567656798555, 2.3362589721268705)]
        for lat,lon in go_list_zone2_bretigny:
            url_go_to = f"https://app.uavia.eu/robotscontrolwebservice/api/{id}/navigation/go"
            go_to_target = {
            "lat": lat,
            "lng": lon,
            "alt": altitude,
            "isRelativeAltitude": True,
            "strategy": "GOTO_STRATEGY_NONE"
            }
            response = self.chrome_session.put(url_go_to,json=go_to_target)

            print(f"go_to_api : ",response.status_code)
            time.sleep(2)
        self.delete_poi_api(id=id)
        

def main_test(environnement,site,robot_name,robot_id,action_type,is_simu,headless):

    tester1 = End2EndTester(headless)
    title_page = "Robotics Platform"

    #Manual 
    # APP config 
    (URP_app_link,userInfo) = tester1.readConfig("APP")
    # URP_SITE_TITLE = "BRETIGNY - DEMO"
    # ROBOT_NAME = "SimulatorA"
    # ROBOT_SIM = True
    #ROBOT_NAME = "DJI-M300-004"
    #ROBOT_NAME = "ANAFI-AI003212"

    # DEV config
    # (URP_app_link,userInfo) = readConfig("DEV")
    # URP_SITE_TITLE = "BA 217 Bretigny-sur-Orge"
    # ROBOT_NAME = "Simulator GG"
    # specific_button_index = 44

    # Auto
    (URP_app_link,userInfo) = tester1.readConfig(environnement)
    URP_SITE_TITLE = site
    ROBOT_NAME = robot_name
    ROBOT_SIM = is_simu


    tester1.goToWebPage(url_link=URP_app_link)

    time.sleep (2)

    tester1.verifyTitleWebFN(title_page=title_page)

    tester1.LoginFN(userInfo=userInfo)

    time.sleep(2)

    try:
        
        while True: 
            
            list_of_button_info_robot = tester1.driver.find_elements(By.XPATH, tester1.ROBOT_INFORMATION_BUTTON)
            list_of_button_fly_now_robot = tester1.driver.find_elements(By.XPATH, tester1.ROBOT_FLY_BUTTON)  
            print(f"Nombre de button information robot = {len(list_of_button_info_robot)}")
            print(f"Nombre de button flynow robot = {len(list_of_button_fly_now_robot)}")
            
            time.sleep(3)

            # Site Name Verification :
            tester1.siteNameVerificationFN(site_name=URP_SITE_TITLE)

            # Side Bar Navigation : 
            # tester1.sidebarNavigationFN()
            
            # Robot Informations
            #tester1.robotInfoPageVerification(

            # Sites Verification
            # tester1.sideTabVerificationFN(

            # Site Name Verification :
            # tester1.siteNameVerificationFN(site_name=URP_SITE_TITLE)
            time.sleep(5)

            # Launch Mission 
            launch_flag = tester1.launchMissionRobotFN(name=ROBOT_NAME)
            if not(launch_flag) :
                exit()

            # Mission Action
            if action_type == 1 :
                tester1.loop_action(robot_simu=ROBOT_SIM,id=robot_id)
            elif action_type == 2 : 
                tester1.actionMissionFN(robot_simu=ROBOT_SIM,id=robot_id)
            tester1.driver.quit()
            break
            


    except KeyboardInterrupt:
        print("Arrêt du script par l'utilisateur.")
    finally:
        tester1.driver.quit()

    #tester1.driver.quit()
