from flask import Flask, render_template, request, send_file,jsonify
import qrcode
from PIL import Image
from werkzeug.utils import secure_filename
from flask_cors  import CORS
import os
import cv2
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO


app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/telefone')
def telefone():
    return render_template('telefone.html')

@app.route('/sms')
def sms():
    return render_template('sms.html')

@app.route('/wifi')
def wifi():
    return render_template('wifi.html')

@app.route('/cartVi')
def cartvis():
    return render_template('cartvis.html')

@app.route('/whatsapp')
def whatsapp():
    return render_template('whatsapp.html')

@app.route('/localizacao')
def localizacao():
    return render_template('localizacao.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

def generate_random_subdomain(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

@app.route('/gerar_qrcode', methods=['POST'])
def gerar_qrcode():
    link = request.form['link']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']

    tamanho_fixo = 300

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()

    novos_pixels = []
    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)

    logo = None

    if file and file.filename != '':
        logo = Image.open(file)
   
    if logo:
        basewidth = int(imagem.size[0] / 4)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)

    nome_arquivo = "qrcode_com_logo.png"
    imagem.save(nome_arquivo, "PNG")

    return send_file(nome_arquivo, as_attachment=True)




@app.route('/gerar_qrcode_email', methods=['POST'])
def gerar_qrcode_email():
    email = request.form['email']
    assunto = request.form['assunto']
    mensagem = request.form['mensagem']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']

    # Criar o conteúdo do QR Code
    conteudo = f"mailto:{email}?subject={assunto}&body={mensagem}"
    
    tamanho_fixo = 300

    # Criar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)

    # Criar a imagem do QR Code
    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()

    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)
    
    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)


    nome_arquivo = "qrcode_transparente.png"
    imagem.save(nome_arquivo, "PNG")

    # Enviar o arquivo para download
    return send_file(nome_arquivo, as_attachment=True)


@app.route('/gerar_qrcode_telefone', methods=['POST'])
def gerar_qrcode_telefone():
    codigo_pais = request.form['codigoPais']
    numero_telefone = request.form['numeroTelefone']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']

    # Criar o conteúdo do QR Code (no formato de um link de chamada telefônica)
    conteudo = f"tel:+{codigo_pais}{numero_telefone}"
    
    tamanho_fixo = 300

    # Criar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)

    # Criar a imagem do QR Code
    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()

    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)
    
    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)


    nome_arquivo = "qrcode_telefone.png"
    imagem.save(nome_arquivo, "PNG")

    # Enviar o arquivo para download
    return send_file(nome_arquivo, as_attachment=True)

@app.route('/gerar_qrcode_sms', methods=['POST'])
def gerar_qrcode_sms():
    codigo_pais = request.form['codigoPais']
    dd_estado = request.form['DDEstado']
    numero_telefone = request.form['numeroTelefone']
    mensagem = request.form['mensagem']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']
    

    # Criar o conteúdo do QR Code (no formato de um link para enviar SMS)
    conteudo = f"sms:+{codigo_pais}{dd_estado}{numero_telefone}?body={mensagem}"
    
    tamanho_fixo = 300

    # Criar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)

    # Criar a imagem do QR Code
    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()


    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)
    
    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)


    nome_arquivo = "qrcode_sms.png"
    imagem.save(nome_arquivo, "PNG")

    # Enviar o arquivo para download
    return send_file(nome_arquivo, as_attachment=True)

@app.route('/gerar_qrcode_wifi', methods=['POST'])
def gerar_qrcode_wifi():
    nome_rede = request.form['nomeRede']
    tipo_seguranca = request.form['tipoSeguranca']
    senha = request.form['senha']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']

    # Criar o conteúdo do QR Code (no formato de configuração de Wi-Fi)
    conteudo = f"WIFI:T:{tipo_seguranca};S:{nome_rede};P:{senha};;"
    
    tamanho_fixo = 300

    # Criar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)

    # Criar a imagem do QR Code
    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()

    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)
    
    
    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)


    nome_arquivo = "qrcode_wifi.png"
    imagem.save(nome_arquivo, "PNG")

    # Enviar o arquivo para download
    return send_file(nome_arquivo, as_attachment=True)

@app.route('/gerar_qrcode_visita', methods=['POST'])
def gerar_qrcode_visita():
    primeiro_nome = request.form['primeiroNome']
    sobrenome = request.form['sobrenome']
    email = request.form['email']
    url_site = request.form['urlSite']
    nome_empresa = request.form['nomeEmpresa']
    cargo = request.form['cargo']
    cep = request.form['cep']
    endereco = request.form['endereco']
    cidade = request.form['cidade']
    pais = request.form['pais']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']

    # Criar o conteúdo do QR Code (no formato de informações do cartão de visita)
    conteudo = f"BEGIN:VCARD\nVERSION:3.0\nN:{sobrenome};{primeiro_nome};;;\nFN:{primeiro_nome} {sobrenome}\nORG:{nome_empresa}\nTITLE:{cargo}\nTEL;TYPE=WORK,VOICE:\nADR;TYPE=WORK:;;{endereco};{cidade};;{cep};{pais}\nEMAIL:{email}\nURL:{url_site}\nEND:VCARD"

    tamanho_fixo = 300
    
    # Criar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)

    # Criar a imagem do QR Code
    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()


    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)
    
    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)
   

    nome_arquivo = "qrcode_cartao_visita.png"
    imagem.save(nome_arquivo, "PNG")

    # Enviar o arquivo para download
    return send_file(nome_arquivo, as_attachment=True)

@app.route('/gerar_qrcode_whatsapp', methods=['POST'])
def gerar_qrcode_whatsapp():
    codigo_pais = request.form['codigoPais']
    dd_estado = request.form['DDEstado']
    numero_telefone = request.form['numeroTelefone']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']
    

    # Criar o conteúdo do QR Code (no formato de um link para enviar SMS)
    conteudo = f"wa.me/+{codigo_pais}{dd_estado}{numero_telefone}"
    
    tamanho_fixo = 300

    # Criar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)

    # Criar a imagem do QR Code
    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()


    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)
    
    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)
   

    nome_arquivo = "qrcode_sms.png"
    imagem.save(nome_arquivo, "PNG")

    # Enviar o arquivo para download
    return send_file(nome_arquivo, as_attachment=True)

@app.route('/gerar_qrcode_localizacao', methods=['POST'])
def gerar_qrcode_localizacao():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']
    
    
    link = f"https://www.google.com/maps?q={latitude},{longitude}"
    
    tamanho_fixo = 300

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()


    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)
    
    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)


    nome_arquivo = "qrcode_localizacao.png"
    imagem.save(nome_arquivo, "PNG")

    # Enviar o arquivo para download
    return send_file(nome_arquivo, as_attachment=True)




@app.route('/generate', methods=['POST'])
def generate():
    restaurantname = request.form['restaurantname']
    reclogo= request.files['reclogo']
    bglogo= request.files['bglogo']
    entradaname = request.form['entradaname']
    entradaname2 = request.form['entradaname2']
    entradaname3 = request.form['entradaname3']
    entradaname4 = request.form['entradaname4']
    entradaname5 = request.form['entradaname5']
    entradaname6 = request.form['entradaname6']
    entradadescription = request.form['entradadescription']
    entradadescription2 = request.form['entradadescription2']
    entradadescription3 = request.form['entradadescription3']
    entradadescription4 = request.form['entradadescription4']
    entradadescription5 = request.form['entradadescription5']
    entradadescription6 = request.form['entradadescription6']
    entradaprice = request.form['entradaprice']
    entradaprice2 = request.form['entradaprice2']
    entradaprice3 = request.form['entradaprice3']
    entradaprice4 = request.form['entradaprice4']
    entradaprice5 = request.form['entradaprice5']
    entradaprice6 = request.form['entradaprice6']
    p1=request.files['p1']
    p2=request.files['p2']
    p3=request.files['p3']
    p4=request.files['p4']
    p5=request.files['p5']
    p6=request.files['p6']
    pratoprincipalname = request.form['pratoprincipalname']
    pratoprincipalname2 = request.form['pratoprincipalname2']
    pratoprincipalname3 = request.form['pratoprincipalname3']
    pratoprincipalname4 = request.form['pratoprincipalname4']
    pratoprincipalname5 = request.form['pratoprincipalname5']
    pratoprincipalname6 = request.form['pratoprincipalname6']
    pratoprincipaldescription = request.form['pratoprincipaldescription']
    pratoprincipaldescription2 = request.form['pratoprincipaldescription2']
    pratoprincipaldescription3 = request.form['pratoprincipaldescription3']
    pratoprincipaldescription4 = request.form['pratoprincipaldescription4']
    pratoprincipaldescription5 = request.form['pratoprincipaldescription5']
    pratoprincipaldescription6 = request.form['pratoprincipaldescription6']
    pratoprincipalprice = request.form['pratoprincipalprice']
    pratoprincipalprice2 = request.form['pratoprincipalprice2']
    pratoprincipalprice3 = request.form['pratoprincipalprice3']
    pratoprincipalprice4 = request.form['pratoprincipalprice4']
    pratoprincipalprice5 = request.form['pratoprincipalprice5']
    pratoprincipalprice6 = request.form['pratoprincipalprice6']
    p1p = request.files['p1p']
    p1p2  = request.files['p1p2']
    p1p3  = request.files['p1p3']
    p1p4  = request.files['p1p4']
    p1p5  = request.files['p1p5']
    p1p6  = request.files['p1p6']
    sobremesaname = request.form['sobremesaname']
    sobremesaname2 = request.form['sobremesaname2']
    sobremesaname3 = request.form['sobremesaname3']
    sobremesaname4 = request.form['sobremesaname4']
    sobremesaname5 = request.form['sobremesaname5']
    sobremesaname6 = request.form['sobremesaname6']
    sobremesadescription = request.form['sobremesadescription']
    sobremesadescription2 = request.form['sobremesadescription2']
    sobremesadescription3 = request.form['sobremesadescription3']
    sobremesadescription4 = request.form['sobremesadescription4']
    sobremesadescription5 = request.form['sobremesadescription5']
    sobremesadescription6 = request.form['sobremesadescription6']
    sobremesaprice = request.form['sobremesaprice']
    sobremesaprice2 = request.form['sobremesaprice2']
    sobremesaprice3 = request.form['sobremesaprice3']
    sobremesaprice4 = request.form['sobremesaprice4']
    sobremesaprice5 = request.form['sobremesaprice5']
    sobremesaprice6 = request.form['sobremesaprice6']
    p1s = request.files['p1s']
    p1s2 = request.files['p1ps2']
    p1s3 = request.files['p1s3']
    p1s4 = request.files['p1s4']
    p1s5 = request.files['p1s5']
    p1s6 = request.files['p1s6']
    bebidaname = request.form['bebidaname']
    bebidaname2 = request.form['bebidaname2']
    bebidaname3 = request.form['bebidaname3']
    bebidaname4 = request.form['bebidaname4']
    bebidaname5 = request.form['bebidaname5']
    bebidaname6 = request.form['bebidaname6']
    bebidadescription = request.form['bebidadescription']
    bebidadescription2 = request.form['bebidadescription2']
    bebidadescription3 = request.form['bebidadescription3']
    bebidadescription4 = request.form['bebidadescription4']
    bebidadescription5 = request.form['bebidadescription5']
    bebidadescription6 = request.form['bebidadescription6']
    bebidaprice = request.form['bebidaprice']
    bebidaprice2 = request.form['bebidaprice2']
    bebidaprice3 = request.form['bebidaprice3']
    bebidaprice4 = request.form['bebidaprice4']
    bebidaprice5 = request.form['bebidaprice5']
    bebidaprice6 = request.form['bebidaprice6']
    p1b = request.files['p1b']
    p1b2 = request.files['p1b2']
    p1b3 = request.files['p1b3']
    p1b4 = request.files['p1b4']
    p1b5 = request.files['p1b5']
    p1b6 = request.files['p1b6']
    phonenumber = request.form['phonenumber']
    cor_qr = request.form['corQR']
    back_qr = request.form['backQR']
    file = request.files['file']
    subdomain = generate_random_subdomain()
    page_filename = f"{subdomain}.html"
    
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
        
    reclogo.save(os.path.join('static/uploads', reclogo.filename))
    bglogo.save(os.path.join('static/uploads', bglogo.filename))

    if not os.path.exists('templates/generated'):
        os.makedirs('templates/generated')

    with open(os.path.join('templates/generated', page_filename), "w") as f:
        f.write(render_template('page.html', restaurantname=restaurantname, entradaname=entradaname,entradaname2=entradaname2,entradaname3=entradaname3,entradaname4=entradaname4,
                                entradaname5=entradaname5,entradaname6=entradaname6,entradadescription=entradadescription,entradadescription2=entradadescription2,entradadescription3=entradadescription3,
                                entradadescription4=entradadescription4, entradadescription5=entradadescription5, entradadescription6=entradadescription6, entradaprice=entradaprice,entradaprice2=entradaprice2,
                                entradaprice3=entradaprice3,entradaprice4=entradaprice4,entradaprice5=entradaprice5,entradaprice6=entradaprice6,p1=p1,p2=p2,p3=p3,p4=p4,p5=p5,p6=p6,reclogo=reclogo,bglogo=bglogo,
                                pratoprincipalname=pratoprincipalname ,pratoprincipalname2=pratoprincipalname2,pratoprincipalname3=pratoprincipalname3,pratoprincipalname4=pratoprincipalname4,pratoprincipalname5=pratoprincipalname5,pratoprincipalname6=pratoprincipalname6
                                ,pratoprincipaldescription=pratoprincipaldescription,pratoprincipaldescription2=pratoprincipaldescription2,pratoprincipaldescription3=pratoprincipaldescription3,
                                pratoprincipaldescription4=pratoprincipaldescription4,pratoprincipaldescription5=pratoprincipaldescription5,pratoprincipaldescription6=pratoprincipaldescription6, pratoprincipalprice=pratoprincipalprice,pratoprincipalprice2=pratoprincipalprice2,pratoprincipalprice3=pratoprincipalprice3,
                                pratoprincipalprice4=pratoprincipalprice4,pratoprincipalprice5=pratoprincipalprice5,pratoprincipalprice6=pratoprincipalprice6,p1p=p1p,p1p2=p1p2,p1p3=p1p3,p1p4=p1p4,p1p5=p1p5,p1p6=p1p6,
                                sobremesaname=sobremesaname,sobremesaname2=sobremesaname2,sobremesaname3=sobremesaname3,sobremesaname4=sobremesaname4,sobremesaname5=sobremesaname5,sobremesaname6=sobremesaname6,
                                sobremesadescription=sobremesadescription,sobremesadescription2=sobremesadescription2,sobremesadescription3=sobremesadescription3,sobremesadescription4=sobremesadescription4,
                                sobremesadescription5=sobremesadescription5,sobremesadescription6=sobremesadescription6, sobremesaprice=sobremesaprice,sobremesaprice2=sobremesaprice2,sobremesaprice3=sobremesaprice3,sobremesaprice4=sobremesaprice4,
                                sobremesaprice5=sobremesaprice5,sobremesaprice6=sobremesaprice6,p1s=p1s,p1s2=p1s2,p1s3=p1s3,p1s4=p1s4,p1s5=p1s5,p1s6=p1s6,
                                bebidaname=bebidaname,bebidaname2=bebidaname2,bebidaname3=bebidaname3,bebidaname4=bebidaname4,bebidaname5=bebidaname5,bebidaname6=bebidaname6,bebidadescription=bebidadescription,bebidadescription2=bebidadescription2,bebidadescription3=bebidadescription3,
                                bebidadescription4=bebidadescription4,bebidadescription5=bebidadescription5,bebidadescription6=bebidadescription6, bebidaprice=bebidaprice,bebidaprice2=bebidaprice2,bebidaprice3=bebidaprice3,bebidaprice4=bebidaprice4,
                                bebidaprice5=bebidaprice5,bebidaprice6=bebidaprice6,p1b=p1b,p1b2=p1b2,p1b3=p1b3,p1b4=p1b4,p1b5=p1b5,p1b6=p1b6, phonenumber=phonenumber))

    tamanho_fixo = 300

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    full_url = f"{request.url_root}pages/{subdomain}"
    qr.add_data(full_url)
    qr.make(fit=True)

    imagem = qr.make_image(fill_color=cor_qr, back_color=back_qr).resize((tamanho_fixo, tamanho_fixo))
    imagem = imagem.convert("RGBA")
    pixels = imagem.getdata()

    novos_pixels = []

    for pixel in pixels:
        r, g, b, a = pixel
        novos_pixels.append((r, g, b))

    imagem.putdata(novos_pixels)

    if file:
        logo = Image.open(file)
        basewidth = int(imagem.size[0] / 5)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((imagem.size[0] - logo.size[0]) // 2, (imagem.size[1] - logo.size[1]) // 2)
        imagem.paste(logo, pos, mask=logo.split()[3] if logo.mode == 'RGBA' else None)

    buffer = BytesIO()
    imagem.save(buffer, 'PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
@app.route('/pages/<subdomain>')
def show_page(subdomain):
    try:
        return render_template(f"generated/{subdomain}.html")
    except:
        return "Page not found", 404

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    
    # Configurações do email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'qrcodemastercombr@gmail.com'
    smtp_password = 'xxlh iwcq pxez bwvn'

    # Configurar o email
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'qrcodemastercombr@gmail.com'
    msg['Subject'] = subject

    body = f'Nome: {name}\nEmail: {email}\n\n{message}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Enviar o email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, 'qrcodemastercombr@gmail.com', text)
        server.quit()

        return render_template('success.html')
    except Exception as e:
        print(f'Erro ao enviar email: {e}')
        return 'Erro ao enviar o formulário.'

    
if __name__ == '__main__':
    app.run(debug=True)
