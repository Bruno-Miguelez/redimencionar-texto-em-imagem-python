import cv2
import numpy as np
import textwrap
import unicodedata

class ImagemTexto():
    def __init__(self, texto = "abc", fonte = cv2.FONT_HERSHEY_COMPLEX, tamanho_fonte = 3, grossura = 1, largura = 1800, altura = 1800, margem = 40, bordas = 100, corTexto = (255,255,255), corImagem = (30,30,30)):


        def wrap(text, width):
            out = textwrap.wrap(text, width, replace_whitespace = False)
            out2 = []
            for i in range(0, len(out)):
                out2 = [*out2, *out[i].split("\n")]

            return out2
                    
        
        def darTamanhoFonte(texto, fonte, tamanho_fonte, grossura, largura, altura, margem, bordas):
            min_ = 0
            max_ = tamanho_fonte

            while min_ < max_ - 0.0001:
                alvo = (min_ + max_) / 2

                letraEmPx = cv2.getTextSize(texto, fonte, alvo, grossura)[0][0] / len(texto)
                letrasPorLinha = (largura - bordas * 2) // letraEmPx
                linhas = wrap(texto, letrasPorLinha)

            
                alturaLinha = cv2.getTextSize(texto, fonte, alvo, grossura)[0][1] + margem
                alturaTexto = alturaLinha * len(linhas)

                #print(alturaTexto)
                #print(min_)
                #print(max_)
                #print("")

                if alturaTexto > altura:
                    max_ = alvo

                elif alturaTexto < altura:
                    min_ = alvo
                    
                else:
                    return alvo

            if alturaTexto > altura:
                alvo = min_

            return alvo

        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore')
        texto = texto.decode("utf-8")
        
        letraEmPx = cv2.getTextSize(texto, fonte, tamanho_fonte, grossura)[0][0] / len(texto)
        letrasPorLinha = (largura - bordas * 2) // letraEmPx
        linhas = wrap(texto, letrasPorLinha)

        larguraLinha, alturaLinha = cv2.getTextSize(texto, fonte, tamanho_fonte, grossura)[0]
        alturaLinha += margem

        if(alturaLinha * len(linhas) > altura):
            tamanho_fonte = darTamanhoFonte(texto, fonte, tamanho_fonte, grossura, largura, altura, margem, bordas)

            letraEmPx = cv2.getTextSize(texto, fonte, tamanho_fonte, grossura)[0][0] / len(texto)
            letrasPorLinha = (largura - bordas * 2) // letraEmPx
            linhas = wrap(texto, letrasPorLinha)
            
            larguraLinha, alturaLinha = cv2.getTextSize(linhas[0], fonte, tamanho_fonte, grossura)[0]
            alturaLinha += margem

        img = np.zeros((largura + bordas * 2, altura + bordas * 2, 3))
        img[:] = corImagem

        for i in range(len(linhas)):
            cv2.putText(img, linhas[i], (0 + bordas, alturaLinha * (i + 1) + bordas), fonte, tamanho_fonte, corTexto, grossura)

        self.img =  img

        
    def salvar(self, nome = "output.png", caminho = ""):
        cv2.imwrite(caminho + nome, self.img)

text = """texto"""
print("text to image")
teste = ImagemTexto(texto = text, grossura = 2)
#cv2.imshow("img", teste.img)
teste.salvar()

