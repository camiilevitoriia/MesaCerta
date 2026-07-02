import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestMesaCerta(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "http://127.0.0.1:5000"

    def tearDown(self):
        self.driver.quit()

    #teste 1
    def test_cadastro_com_sucesso(self):

        driver = self.driver
        driver.get(f"{self.base_url}/comandas")

        driver.find_element(By.ID, "cliente").send_keys("Carlos Alencar")
        driver.find_element(By.ID, "mesa").send_keys("4")
        driver.find_element(By.ID, "pedido").send_keys("Suco de Laranja e Pastel")
        driver.find_element(By.ID, "quantidade").send_keys("2")
        driver.find_element(By.ID, "valor").send_keys("12.50")
        
        driver.find_element(By.ID, "btnCadastrar").click()
        time.sleep(1.5)

        elemento_msg = driver.find_element(By.ID, "mensagem")
        self.assertEqual(elemento_msg.text, "Comanda cadastrada com sucesso!")
        
        corpo_tabela = driver.find_element(By.ID, "corpoTabela")
        self.assertIn("Carlos Alencar", corpo_tabela.text)
   
    #teste 2
    def test_validacao_quantidade_invalida(self):
        driver = self.driver
        driver.get(f"{self.base_url}/comandas")

        # Injeta o novalidate via JS para ignorar a trava do HTML5 nativo do Chrome
        driver.execute_script("document.getElementById('formComanda').setAttribute('novalidate', 'true');")

        driver.find_element(By.ID, "cliente").send_keys("Juliana Costa")
        driver.find_element(By.ID, "mesa").send_keys("7")
        driver.find_element(By.ID, "pedido").send_keys("X-Burguer")
        driver.find_element(By.ID, "quantidade").send_keys("0")  # Inválido
        driver.find_element(By.ID, "valor").send_keys("22.00")
        
        driver.find_element(By.ID, "btnCadastrar").click()
        time.sleep(1)

        elemento_msg = driver.find_element(By.ID, "mensagem")
        self.assertEqual(elemento_msg.text, "A quantidade deve ser maior que zero.")
        self.assertIn("erro", elemento_msg.get_attribute("class"))
    
    #teste 3
    def test_navegacao_entre_paginas(self):
        driver = self.driver
        
        driver.get(f"{self.base_url}/")
        self.assertIn("Início - Mesa Certa", driver.title)

        link_comandas = driver.find_element(By.LINK_TEXT, "Comandas")
        link_comandas.click()
        
        self.assertEqual(driver.current_url, f"{self.base_url}/comandas")

if __name__ == "__main__":
    unittest.main()