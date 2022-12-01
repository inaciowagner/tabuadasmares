from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pyautogui
import pyperclip


browser = webdriver.Chrome()
browser.get("https://tabuademares.com/br/rio-grande-do-norte/areia-branca#_mares")  # abre site tabuadasmares.com.br
time.sleep(5)                                                                       # time.sleep é um intervalo para espera de que as páginas carregem
browser.find_element(By.XPATH,'//*[@id="botones_cookies"]/a[2]').click()    # clica no "ok" pra aceitar cookies
time.sleep(2)

for i in range (3):
    pyautogui.click(x=678, y=341)       # seleciona o texto

pyautogui.hotkey("ctrl", "c")           # copia o texto

browser.get("https://outlook.live.com/mail/0/") # abre hotmail

browser.find_element(By.XPATH,'/html/body/header/div/aside/div/nav/ul/li[2]/a').click()     #clica no botão "entrar"
time.sleep(3)
browser.find_element(By.XPATH,'//*[@id="i0116"]').send_keys("inaciowagner@hotmail.com")         # preenche o campo "e-mail" configure com seus dados (este código está configurado para hotmail ou outro dominio da Microsoft como outlook.com)
browser.find_element(By.XPATH,'//*[@id="i0116"]').send_keys(Keys.ENTER)                     # dá enter no e-mail
time.sleep(5)
browser.find_element(By.XPATH,'//*[@id="i0118"]').send_keys("******")                        # digita senha     configure sua senha
browser.find_element(By.XPATH,'//*[@id="idSIButton9"]').click()                             # submete a senha
time.sleep(5)


pyautogui.press("enter")    # fecha a janela que pergunta se quer continuar conectado no hotmail
time.sleep(10)

browser.find_element(By.XPATH,'//*[@id="id__9"]').click()   # clica pra começar a digitar a mensagem
time.sleep(2)
browser.find_element(By.XPATH,'//*[@id="docking_InitVisiblePart_0"]/div/div[1]/div[1]/div/div[3]/div/div/div[1]').send_keys("beeblebrox@gmail.com")     # digita e-mail do destinatário
time.sleep(1)
pyautogui.press("enter")    # dá enter no destinatário
pyautogui.press("tab")      # pula pro campo "assunto"
pyautogui.write("informações de tábua das marés")   # digita o assunto
pyautogui.press("tab")                              # pua pro campo de digitação do corpo do e-mail / mensagem
time.sleep(1)
pyautogui.hotkey("ctrl", "v")                       # cola o texto capturado no site da tábua das marés
pyautogui.write("Fone tabuademares.com")           # cita fonte da informação
pyautogui.press("enter")                            # quebra de linha
pyautogui.write("atenciosamente, Inacio Wagner")    # assina o e-mail
time.sleep(5)                                       # Deletar esta linha que é apenas para demonstração do código - um tempo para visuailzar a mensgem escrita
pyautogui.hotkey("ctrl", "enter")                   # envia a mensagem
pyautogui.press("entar")                            # fecha janelinha de alerta
time.sleep(3)

browser.close()
