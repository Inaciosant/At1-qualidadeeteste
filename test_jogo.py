import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def testar_joguinho():
    driver = webdriver.Chrome()

    try:
        caminho_arquivo = "file://" + os.path.abspath("Jogo_desafio.html")
        driver.get(caminho_arquivo)

        elemento_esperado = driver.find_element(By.ID, "numeroEsperado")
        botao_clique = driver.find_element(By.ID, "incrementador")
        div_resultado = driver.find_element(By.ID, "resultado")

        numero_esperado_texto = elemento_esperado.text

        assert numero_esperado_texto != "", \
            "Falha: o número esperado não apareceu na tela"

        print("Cenário 1: número esperado aparece na tela")

        numero_esperado = int(numero_esperado_texto)

        assert 1 <= numero_esperado <= 20, \
            "Falha: número esperado fora do intervalo de 1 a 20"

        print("Cenário 2: número esperado está entre 1 e 20")
        print(f"Número esperado: {numero_esperado}")

        paragrafos_iniciais = div_resultado.find_elements(By.TAG_NAME, "p")

        assert len(paragrafos_iniciais) == 0, \
            "Falha: o jogo iniciou com resultados na tela"

        print("Cenário 3: jogo iniciou sem resultados")

        assert botao_clique.text == "Clique aqui", \
            "Falha: texto do botão/link está incorreto"

        print("Cenário 4: botão/link encontrado corretamente")

        ganhou = False
        tentativas = 0

        cenario_5_impresso = False
        cenario_6_impresso = False
        cenario_7_impresso = False

        while not ganhou:
            quantidade_antes = len(div_resultado.find_elements(By.TAG_NAME, "p"))

            botao_clique.click()
            tentativas += 1

            paragrafos = div_resultado.find_elements(By.TAG_NAME, "p")
            quantidade_depois = len(paragrafos)

            assert quantidade_depois == quantidade_antes + 1, \
                "Falha: o clique não adicionou um novo resultado"

            if not cenario_5_impresso:
                print("Cenário 5: cada clique adiciona um novo resultado")
                cenario_5_impresso = True

            ultimo_paragrafo = paragrafos[-1].text

            texto_numero = ultimo_paragrafo.replace(" - Você ganhou!!!", "")
            numero_sorteado = int(texto_numero)

            assert 1 <= numero_sorteado <= 20, \
                "Falha: número sorteado fora do intervalo de 1 a 20"

            if not cenario_6_impresso:
                print("Cenário 6: número sorteado está entre 1 e 20")
                cenario_6_impresso = True

            if "Você ganhou!!!" in ultimo_paragrafo:
                assert numero_sorteado == numero_esperado, \
                    "Falha: o jogo deu vitória para o número errado"

                ganhou = True

                print(f"Cenário 8: vitória correta após {tentativas} tentativas")
                print(f"Texto da vitória: {ultimo_paragrafo}")

            else:
                assert "Você ganhou!!!" not in ultimo_paragrafo, \
                    "Falha: mensagem de vitória apareceu antes da hora"

                assert numero_sorteado != numero_esperado, \
                    "Falha: número esperado saiu, mas a mensagem de vitória não apareceu"

                if not cenario_7_impresso:
                    print("Cenário 7: mensagem de vitória não aparece antes da hora")
                    cenario_7_impresso = True

            if tentativas > 500:
                raise Exception("Limite de tentativas excedido. Possível erro no jogo.")

        quantidade_antes_pos_vitoria = len(div_resultado.find_elements(By.TAG_NAME, "p"))

        botao_clique.click()

        paragrafos_pos_vitoria = div_resultado.find_elements(By.TAG_NAME, "p")
        quantidade_depois_pos_vitoria = len(paragrafos_pos_vitoria)

        assert quantidade_depois_pos_vitoria == quantidade_antes_pos_vitoria + 1, \
            "Falha: clique pós-vitória não adicionou a mensagem"

        ultimo_paragrafo_pos = paragrafos_pos_vitoria[-1].text

        assert ultimo_paragrafo_pos == "Você já ganhou, pare de clicar!", \
            f"Falha no pós-vitória. Texto recebido: '{ultimo_paragrafo_pos}'"

        print("Cenário 9: clique após a vitória mostra a mensagem correta")
        print(f"Texto pós-vitória: {ultimo_paragrafo_pos}")

        print("\nSUCESSO: Todos os cenários foram testados e validados!")

    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    testar_joguinho()