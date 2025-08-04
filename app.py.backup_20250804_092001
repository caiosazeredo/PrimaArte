# -*- coding: utf-8 -*-
"""
🎨 PRIMA ARTE - APLICAÇÃO PRINCIPAL
==================================
Site de artesanato feito à mão
Desenvolvido para Valéria & Flávia
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import os
import urllib.parse
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'prima-arte-secret-key-2025'

# Configurações
WHATSAPP_NUMBER = '+5521973108293'
INSTAGRAM_URL = 'https://www.instagram.com/primaarte2025/'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Base de dados simples em JSON
DATA_FILE = 'data.json'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'products': [],
        'announcements': [],
        'admin_password': 'primaarte2025'
    }

def save_data(data):
    """Salva dados no arquivo JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_slug(text):
    """Cria slug amigável para URL"""
    import re
    import unicodedata
    
    # Remove acentos
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    
    # Converte para minúsculas e substitui espaços e caracteres especiais por hífen
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    text = text.strip('-')
    
    return text

@app.template_filter('slug')
def slug_filter(text):
    """Filtro para criar slugs"""
    return create_slug(text)

# Função auxiliar para gerar URL do produto
@app.template_global()
def product_url(product):
    """Gera URL amigável para produto"""
    return url_for('product_detail', product_slug=create_slug(product['name']))

# ================================
# ROTAS PRINCIPAIS
# ================================

@app.route('/')
def index():
    """Página inicial"""
    data = load_data()
    featured_products = [p for p in data['products'] if p.get('featured', False)][:6]
    announcements = [a for a in data['announcements'] if a.get('active', True)][:3]
    return render_template('index.html', 
                         featured_products=featured_products,
                         announcements=announcements)

@app.route('/produtos')
def products():
    """Página de produtos"""
    data = load_data()
    category = request.args.get('categoria', '')
    products = data['products']
    
    if category:
        products = [p for p in products if p.get('category', '').lower() == category.lower()]
    
    return render_template('products.html', 
                         products=products, 
                         current_category=category)

@app.route('/produto/<product_slug>')
def product_detail(product_slug):
    """Detalhes do produto com slug amigável ou ID"""
    data = load_data()
    
    # Primeiro tenta encontrar por slug, depois por ID para compatibilidade
    product = None
    for p in data['products']:
        product_slug_generated = create_slug(p['name'])
        if product_slug_generated == product_slug or p['id'] == product_slug:
            product = p
            break
    
    if not product:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('products'))
    
    return render_template('product.html', product=product)

@app.route('/carrinho')
def cart():
    """Página do carrinho"""
    cart_items = session.get('cart', [])
    data = load_data()
    
    # Busca detalhes dos produtos no carrinho
    detailed_cart = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            detailed_cart.append({
                'id': item['product_id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': item['quantity'],
                'total': item_total,
                'images': product.get('images', []),
                'description': item.get('description', '')
            })
            total += item_total
    
    return render_template('cart.html', cart_items=detailed_cart, total=total)

@app.route('/adicionar-carrinho', methods=['POST'])
def add_to_cart():
    """Adiciona produto ao carrinho"""
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    description = request.form.get('description', '')
    
    if 'cart' not in session:
        session['cart'] = []
    
    # Verifica se produto já está no carrinho
    cart = session['cart']
    existing_item = next((item for item in cart if item['product_id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        cart.append({
            'product_id': product_id,
            'quantity': quantity,
            'description': description
        })
    
    session['cart'] = cart
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('cart'))

@app.route('/remover-carrinho/<product_id>')
def remove_from_cart(product_id):
    """Remove produto do carrinho"""
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
        flash('Produto removido do carrinho!', 'info')
    return redirect(url_for('cart'))

@app.route('/finalizar-pedido')
def checkout():
    """Redireciona para WhatsApp com detalhes do pedido"""
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Seu carrinho está vazio!', 'error')
        return redirect(url_for('cart'))
    
    data = load_data()
    
    # Monta mensagem para WhatsApp (SEM escape de caracteres)
    message = "*🎨 NOVO PEDIDO - PRIMA ARTE*\n\n"
    total = 0
    
    for item in cart_items:
        product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            total += item_total
            
            message += f"📦 *{product['name']}*\n"
            message += f"   Quantidade: {item['quantity']}\n"
            message += f"   Preço: R$ {product['price']:.2f}\n"
            if item.get('description'):
                message += f"   Obs: {item['description']}\n"
            message += f"   Subtotal: R$ {item_total:.2f}\n\n"
    
    message += f"💰 *TOTAL: R$ {total:.2f}*\n\n"
    message += "Olá! Gostaria de finalizar este pedido! 😊"
    
    # URL do WhatsApp com encoding correto
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '').replace(' ', '')}?text={urllib.parse.quote(message)}"
    
    # Limpa carrinho após enviar
    session['cart'] = []
    
    return redirect(whatsapp_url)

# ================================
# ÁREA ADMINISTRATIVA
# ================================

@app.route('/admin')
def admin_login():
    """Página de login do admin"""
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    """Autentica admin"""
    password = request.form.get('password')
    data = load_data()
    
    if password == data.get('admin_password', 'primaarte2025'):
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Senha incorreta!', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Dashboard administrativo"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    stats = {
        'total_products': len(data['products']),
        'total_announcements': len(data['announcements']),
        'active_announcements': len([a for a in data['announcements'] if a.get('active', True)])
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/produtos')
def admin_products():
    """Gerenciar produtos"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    return render_template('admin/products.html', products=data['products'])

@app.route('/admin/produto/novo')
def admin_new_product():
    """Novo produto"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin/product_form.html')

@app.route('/admin/produto/editar/<product_id>')
def admin_edit_product(product_id):
    """Editar produto"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    
    if not product:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', product=product)

@app.route('/admin/produto/excluir/<product_id>')
def admin_delete_product(product_id):
    """Excluir produto"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    
    # Remove produto e suas imagens
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    if product and product.get('images'):
        for image_url in product['images']:
            if image_url.startswith('/static/uploads/'):
                image_path = image_url[1:]  # Remove /
                if os.path.exists(image_path):
                    os.remove(image_path)
    
    data['products'] = [p for p in data['products'] if p['id'] != product_id]
    save_data(data)
    
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/produto/salvar', methods=['POST'])
def admin_save_product():
    """Salva produto com múltiplas imagens"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    
    # Pega dados do formulário
    product_id = request.form.get('id') or str(uuid.uuid4())
    product_name = request.form.get('name')
    
    # Processa upload de múltiplas imagens
    uploaded_images = []
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Adiciona timestamp para evitar conflitos
                filename = f"{int(datetime.now().timestamp())}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                uploaded_images.append(f"/static/uploads/{filename}")
    
    # Se está editando, mantém imagens existentes se não houver novas
    existing_product = next((p for p in data['products'] if p['id'] == product_id), None)
    if existing_product and not uploaded_images:
        uploaded_images = existing_product.get('images', [])
    
    product = {
        'id': product_id,
        'name': product_name,
        'description': request.form.get('description'),
        'price': float(request.form.get('price')),
        'category': request.form.get('category'),
        'images': uploaded_images,
        'featured': request.form.get('featured') == 'on',
        'created_at': existing_product.get('created_at', datetime.now().isoformat()) if existing_product else datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    # Atualiza ou adiciona produto
    existing_index = next((i for i, p in enumerate(data['products']) if p['id'] == product['id']), None)
    if existing_index is not None:
        data['products'][existing_index] = product
    else:
        data['products'].append(product)
    
    save_data(data)
    flash(f'Produto "{product_name}" salvo com sucesso!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/anuncios')
def admin_announcements():
    """Gerenciar anúncios"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    return render_template('admin/announcements.html', announcements=data['announcements'])

@app.route('/admin/anuncio/novo')
def admin_new_announcement():
    """Novo anúncio"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin/announcement_form.html')

@app.route('/admin/anuncio/editar/<announcement_id>')
def admin_edit_announcement(announcement_id):
    """Editar anúncio"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    announcement = next((a for a in data['announcements'] if a['id'] == announcement_id), None)
    
    if not announcement:
        flash('Anúncio não encontrado!', 'error')
        return redirect(url_for('admin_announcements'))
    
    return render_template('admin/announcement_form.html', announcement=announcement)

@app.route('/admin/anuncio/excluir/<announcement_id>')
def admin_delete_announcement(announcement_id):
    """Excluir anúncio"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    
    # Remove anúncio e sua imagem
    announcement = next((a for a in data['announcements'] if a['id'] == announcement_id), None)
    if announcement and announcement.get('image'):
        if announcement['image'].startswith('/static/uploads/'):
            image_path = announcement['image'][1:]  # Remove /
            if os.path.exists(image_path):
                os.remove(image_path)
    
    data['announcements'] = [a for a in data['announcements'] if a['id'] != announcement_id]
    save_data(data)
    
    flash('Anúncio excluído com sucesso!', 'success')
    return redirect(url_for('admin_announcements'))

@app.route('/admin/anuncio/salvar', methods=['POST'])
def admin_save_announcement():
    """Salva anúncio com imagem"""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    data = load_data()
    
    # Pega dados do formulário
    announcement_id = request.form.get('id') or str(uuid.uuid4())
    announcement_title = request.form.get('title')
    
    # Processa upload de imagem
    uploaded_image = ''
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Adiciona timestamp para evitar conflitos
            filename = f"{int(datetime.now().timestamp())}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            uploaded_image = f"/static/uploads/{filename}"
    
    # Se está editando, mantém imagem existente se não houver nova
    existing_announcement = next((a for a in data['announcements'] if a['id'] == announcement_id), None)
    if existing_announcement and not uploaded_image:
        uploaded_image = existing_announcement.get('image', '')
    
    announcement = {
        'id': announcement_id,
        'title': announcement_title,
        'content': request.form.get('content'),
        'image': uploaded_image,
        'active': request.form.get('active') == 'on',
        'created_at': existing_announcement.get('created_at', datetime.now().isoformat()) if existing_announcement else datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    # Atualiza ou adiciona anúncio
    existing_index = next((i for i, a in enumerate(data['announcements']) if a['id'] == announcement['id']), None)
    if existing_index is not None:
        data['announcements'][existing_index] = announcement
    else:
        data['announcements'].append(announcement)
    
    save_data(data)
    flash(f'Anúncio "{announcement_title}" salvo com sucesso!', 'success')
    return redirect(url_for('admin_announcements'))

@app.route('/admin/logout')
def admin_logout():
    """Logout do admin"""
    session.pop('admin', None)
    return redirect(url_for('index'))

# ================================
# API ENDPOINTS
# ================================

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload de arquivos"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Adiciona timestamp para evitar conflitos
        filename = f"{int(datetime.now().timestamp())}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({'url': f"/static/uploads/{filename}"})
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)