from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json
import requests


# jogadores = []
# gamelist = [{'titulo': 'CS-GO',
#              'ano': 2012,
#              'categoria': 'FPS Online'}]


def init_app(app):
    @app.route('/')
    # View function -> função de visualização
    def home():
        return render_template('index.html')




        # Lista de celulares (que está no site já)
    celulares = [
        {"nome": "iPhone 13", "preco": "R$ 5.999,00", "imagem": "celular1.png"},
        {"nome": "Samsung Galaxy S21", "preco": "R$ 4.499,00", "imagem": "celular2.png"},
        {"nome": "Xiaomi Mi 11", "preco": "R$ 3.999,00", "imagem": "celular3.png"},
        {"nome": "Google Pixel 6", "preco": "R$ 4.299,00", "imagem": "celular4.png"},
        {"nome": "OnePlus 9 Pro", "preco": "R$ 4.799,00", "imagem": "celular5.png"},
        {"nome": "Motorola Edge 20", "preco": "R$ 3.499,00", "imagem": "celular6.png"},
    ]

    @app.route('/produtos', methods=['GET', 'POST'])
    def produtos():
        if request.method == 'POST':
            # Processar o formulário de cadastro de novos celulares
            nome = request.form.get('nome')
            preco = request.form.get('preco')
            imagem = request.form.get('imagem')

            if nome and preco and imagem:
                novo_celular = {
                    "nome": nome,
                    "preco": preco,
                    "imagem": imagem
                }
                celulares.append(novo_celular)
                return redirect(url_for('produtos'))

        return render_template('produtos.html', celulares=celulares)




    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            nome = request.form['nome']
            preco = request.form['preco']
            imagem_url = request.form['imagem_url']

            # Adiciona o celular à lista
            celulares.append({
                'nome': nome,
                'preco': preco,
                'imagem_url': imagem_url
            })

            # Redireciona para a mesma página pra nao duplicar form
            return redirect(url_for('cadastro'))

        # Renderiza a pg
        return render_template('cadastro.html', celulares=celulares)





    @app.route('/consumo', methods=['GET', 'POST'])
    @app.route('/consumo/<int:id>', methods=['GET', 'POST'])
    def consumo():
        # URL da página do GSMArena
        url = "https://www.gsmarena.com/makers.php3"

        try:
            # Cabeçalho
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Requisição HTTP
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Parse do html
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontra as marcas de celulares
            marcas = []
            brand_table = soup.find('table')
            if brand_table:
                for a in brand_table.find_all('a'):
                    marca = {
                        'nome': a.text.strip(),
                        'link': "https://www.gsmarena.com/" + a['href']
                    }
                    marcas.append(marca)
            else:
                return "Erro: Não foi possível encontrar as marcas na página.", 500

            return render_template('consumo.html', marcas=marcas)

        except requests.exceptions.RequestException as e:
            return f"Erro ao acessar a página: {e}", 500
        except Exception as e:
            return f"Erro inesperado: {e}", 500