import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestMesaCerta(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "http://127.0.0.1:5000"
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self):
        self.driver.quit()

    def preencher_formulario(self, cliente, mesa, pedido, quantidade, valor):
        self.driver.find_element(By.ID, "cliente").send_keys(cliente)
        self.driver.find_element(By.ID, "mesa").send_keys(mesa)
        self.driver.find_element(By.ID, "pedido").send_keys(pedido)
        self.driver.find_element(By.ID, "quantidade").send_keys(quantidade)
        self.driver.find_element(By.ID, "valor").send_keys(valor)

    def cadastrar_comanda(self, cliente, mesa, pedido, quantidade, valor):
        self.preencher_formulario(cliente, mesa, pedido, quantidade, valor)
        self.driver.find_element(By.ID, "btnCadastrar").click()

    def aguardar_mensagem(self, texto):
        return self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "mensagem"), texto)
        )

    # teste 1
    def test_cadastro_com_sucesso(self):
        driver = self.driver
        driver.get(f"{self.base_url}/comandas")

        self.cadastrar_comanda(
            "Carlos Alencar",
            "4",
            "Suco de Laranja e Pastel",
            "2",
            "12.50"
        )

        self.aguardar_mensagem("Comanda cadastrada com sucesso!")

        elemento_msg = driver.find_element(By.ID, "mensagem")
        self.assertEqual(elemento_msg.text, "Comanda cadastrada com sucesso!")

        corpo_tabela = driver.find_element(By.ID, "corpoTabela")
        self.wait.until(lambda d: "Carlos Alencar" in corpo_tabela.text)
        self.assertIn("Carlos Alencar", corpo_tabela.text)

    # teste 2
    def test_validacao_quantidade_invalida(self):
        driver = self.driver
        driver.get(f"{self.base_url}/comandas")

        driver.execute_script(
            "document.getElementById('formComanda').setAttribute('novalidate', 'true');"
        )

        self.cadastrar_comanda(
            "Juliana Costa",
            "7",
            "X-Burguer",
            "0",
            "22.00"
        )

        self.aguardar_mensagem("A quantidade deve ser maior que zero.")

        elemento_msg = driver.find_element(By.ID, "mensagem")
        self.assertEqual(elemento_msg.text, "A quantidade deve ser maior que zero.")
        self.assertIn("erro", elemento_msg.get_attribute("class"))

    # teste 3
    def test_navegacao_entre_paginas(self):
        driver = self.driver

        driver.get(f"{self.base_url}/")
        self.assertIn("Início - Mesa Certa", driver.title)

        link_comandas = driver.find_element(By.LINK_TEXT, "Comandas")
        link_comandas.click()

        self.assertEqual(driver.current_url, f"{self.base_url}/comandas")

    # teste 4
    def test_campo_obrigatorio_vazio(self):
        driver = self.driver
        driver.get(f"{self.base_url}/comandas")

        self.preencher_formulario(
            "",
            "3",
            "Refrigerante",
            "1",
            "8.00"
        )

        driver.find_element(By.ID, "btnCadastrar").click()

        campo_cliente = driver.find_element(By.ID, "cliente")

        campo_invalido = driver.execute_script(
            "return arguments[0].validity.valueMissing;",
            campo_cliente
        )

        formulario_invalido = driver.execute_script(
            "return !document.getElementById('formComanda').checkValidity();"
        )

        self.assertTrue(campo_invalido)
        self.assertTrue(formulario_invalido)

    # teste 5
    def test_mensagem_sucesso_exibida(self):
        driver = self.driver
        driver.get(f"{self.base_url}/comandas")

        self.cadastrar_comanda(
            "Marina Souza",
            "9",
            "Lasanha",
            "1",
            "35.00"
        )

        self.aguardar_mensagem("Comanda cadastrada com sucesso!")

        elemento_msg = driver.find_element(By.ID, "mensagem")
        self.assertEqual(elemento_msg.text, "Comanda cadastrada com sucesso!")
        self.assertIn("sucesso", elemento_msg.get_attribute("class"))

    # teste 6
    def test_quantidade_e_ordem(self):
        driver = self.driver
        driver.get(f"{self.base_url}/comandas")

        self.cadastrar_comanda("Ana Teste Ordem", "1", "Pizza", "1", "30.00")
        self.aguardar_mensagem("Comanda cadastrada com sucesso!")

        self.cadastrar_comanda("Bruno Teste Ordem", "2", "Hamburguer", "2", "18.00")
        self.aguardar_mensagem("Comanda cadastrada com sucesso!")

        self.wait.until(
            lambda d: "Ana Teste Ordem" in d.find_element(By.ID, "corpoTabela").text
            and "Bruno Teste Ordem" in d.find_element(By.ID, "corpoTabela").text
        )

        linhas = driver.find_elements(By.CSS_SELECTOR, "#corpoTabela tr")

        linhas_teste = [
            linha for linha in linhas
            if "Teste Ordem" in linha.text
        ]

        self.assertEqual(len(linhas_teste), 2)
        self.assertIn("Ana Teste Ordem", linhas_teste[0].text)
        self.assertIn("Bruno Teste Ordem", linhas_teste[1].text)


if __name__ == "__main__":
    unittest.main()