
# from flask import Flask, send_file
# from PIL import Image 
# import requests
# from io import BytesIO
# import urllib.parse

# app = Flask(__name__)

# @app.route('/overlay/<path:url_imagem_fundo>')
# def overlay_image(url_imagem_fundo):
#     # Decodificar a URL da imagem de fundo
#     url_imagem_fundo = urllib.parse.unquote(url_imagem_fundo)
    
#     # Baixar a imagem de fundo
#     response = requests.get(url_imagem_fundo)
#     imagem_fundo = Image.open(BytesIO(response.content))

#     # Abrir a imagem secundária (imagem de sobreposição)
#     imagem_sobreposta = Image.open("ofertas.png")

#     # Colocar a imagem_sobreposta em cima da imagem_fundo
#     imagem_fundo.paste(imagem_sobreposta, (0, 0), mask=imagem_sobreposta)

#     # Salvar a imagem final em formato PNG
#     imagem_final = BytesIO()
#     imagem_fundo.save(imagem_final, format='PNG')
#     imagem_final.seek(0)

#     # Retornar a imagem final
#     return send_file(imagem_final, mimetype='image/png')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, send_file
from PIL import Image 
import requests
from io import BytesIO
import urllib.parse

app = Flask(__name__)

@app.route('/overlay/<path:url_imagem_fundo>')
def overlay_image(url_imagem_fundo):
    # Decodificar a URL da imagem de fundo
    url_imagem_fundo = urllib.parse.unquote(url_imagem_fundo)
    
    # Baixar a imagem de fundo
    response = requests.get(url_imagem_fundo)
    imagem_fundo = Image.open(BytesIO(response.content))

    # Abrir a imagem secundária (imagem de sobreposição)
    imagem_sobreposta = Image.open("ofertas.png")

    # Redimensionar a imagem de sobreposição para se adaptar ao tamanho da imagem de fundo
    largura_fundo, altura_fundo = imagem_fundo.size
    largura_sobreposta, altura_sobreposta = imagem_sobreposta.size
    fator_redimensionamento = min(largura_fundo / largura_sobreposta, altura_fundo / altura_sobreposta)
    nova_largura = int(largura_sobreposta * fator_redimensionamento)
    nova_altura = int(altura_sobreposta * fator_redimensionamento)
    imagem_sobreposta_redimensionada = imagem_sobreposta.resize((nova_largura, nova_altura))

    # Colocar a imagem_sobreposta no final da imagem_fundo
    posicao_x = largura_fundo - nova_largura
    posicao_y = altura_fundo - nova_altura
    imagem_fundo.paste(imagem_sobreposta_redimensionada, (posicao_x, posicao_y), mask=imagem_sobreposta_redimensionada)

    # Salvar a imagem final em formato PNG
    imagem_final = BytesIO()
    imagem_fundo.save(imagem_final, format='PNG')
    imagem_final.seek(0)

    # Retornar a imagem final
    return send_file(imagem_final, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
