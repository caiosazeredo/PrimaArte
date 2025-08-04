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
from functools import wraps

app = Flask(__name__)
app.secret_key = 'prima-arte-secret-key-2025'

# Configurações
WHATSAPP_NUMBER = '+5521973108293'
INSTAGRAM_URL = 'htt    ps://www.instagram.com/primaarte2025/'
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

def admin_required(f):
    """Decorator para proteger rotas admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

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

# ================================
# FUNÇÕES AUXILIARES PARA PREÇOS
# ================================
def get_product_current_price(product):
    """Retorna o preço atual do produto (promocional se ativo, senão regular)"""
    if product.get('promotion_active') and product.get('promotional_price'):
        return product['promotional_price']
    return product['price']

def calculate_discount_percentage(regular_price, promotional_price):
    """Calcula a porcentagem de desconto"""
    if not promotional_price or promotional_price >= regular_price:
        return 0
    return round(((regular_price - promotional_price) / regular_price) * 100)

# ================================
# FILTROS E FUNÇÕES GLOBAIS PARA TEMPLATES
# ================================
@app.template_filter('slug')
def slug_filter(text):
    """Filtro para criar slugs"""
    return create_slug(text)

@app.template_filter('calculate_discount')
def calculate_discount_filter(regular_price, promotional_price):
    """Calcula desconto para usar nos templates"""
    return calculate_discount_percentage(regular_price, promotional_price)

@app.template_global()
def get_current_price(product):
    """Retorna preço atual do produto para templates"""
    return get_product_current_price(product)

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
    
    # Adiciona preço atual e desconto para cada produto em destaque
    for product in featured_products:
        product['current_price'] = get_product_current_price(product)
        if product.get('promotion_active') and product.get('promotional_price'):
            product['discount_percent'] = calculate_discount_percentage(product['price'], product['promotional_price'])
    
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
    
    # Adiciona preço atual e desconto para cada produto
    for product in products:
        product['current_price'] = get_product_current_price(product)
        if product.get('promotion_active') and product.get('promotional_price'):
            product['discount_percent'] = calculate_discount_percentage(product['price'], product['promotional_price'])
    
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
    
    # Adiciona informações de preço
    product['current_price'] = get_product_current_price(product)
    if product.get('promotion_active') and product.get('promotional_price'):
        product['discount_percent'] = calculate_discount_percentage(product['price'], product['promotional_price'])
        product['savings'] = product['price'] - product['promotional_price']
    
    return render_template('product.html', product=product)

@app.route('/sobre')
def about():
    """Página sobre a Prima Arte"""
    return render_template('about.html')

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
            current_price = get_product_current_price(product)
            item_total = current_price * item['quantity']
            detailed_cart.append({
                'id': item['product_id'],
                'name': product['name'],
                'price': current_price,
                'regular_price': product['price'],
                'promotional_price': product.get('promotional_price'),
                'promotion_active': product.get('promotion_active', False),
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
    
    # Monta mensagem para WhatsApp com formatação melhorada
    message = "*NOVO PEDIDO - PRIMA ARTE*\n"
    message += "═" * 35 + "\n\n"
    
    total = 0
    item_count = 1
    
    for item in cart_items:
        product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
        if product:
            current_price = get_product_current_price(product)
            item_total = current_price * item['quantity']
            total += item_total
            
            message += f"*Item {item_count}:* {product['name']}\n"
            message += f"   • Quantidade: {item['quantity']} unidade(s)\n"
            message += f"   • Preço unitário: R$ {current_price:.2f}\n"
            
            if item.get('description'):
                message += f"   • Observações: {item['description']}\n"
            
            message += f"   • Subtotal: *R$ {item_total:.2f}*\n"
            message += "─" * 30 + "\n"
            item_count += 1
    
    message += f"\n *VALOR TOTAL: R$ {total:.2f}*\n"
    message += "═" * 35 + "\n\n"
    message += " Olá! Gostaria de finalizar este pedido!\n\n"
    message += " *Próximos passos:*\n"
    message += "• Confirmaremos os itens do pedido\n"
    message += "• Combinaremos forma de pagamento\n"
    message += "• Definiremos entrega/retirada\n\n"
    message += " Obrigado por escolher a Prima Arte! "
    
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
@admin_required
def admin_dashboard():
    """Dashboard administrativo"""
    data = load_data()
    stats = {
        'total_products': len(data['products']),
        'total_announcements': len(data['announcements']),
        'active_announcements': len([a for a in data['announcements'] if a.get('active', True)])
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/produtos')
@admin_required
def admin_products():
    """Gerenciar produtos"""
    data = load_data()
    return render_template('admin/products.html', products=data['products'])

@app.route('/admin/produto/novo')
@admin_required
def admin_product_new():
    """Formulário para novo produto"""
    return render_template('admin/product_form.html', product=None)

@app.route('/admin/produto/editar/<product_id>')
@admin_required
def admin_product_edit(product_id):
    """Formulário para editar produto"""
    data = load_data()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    if not product:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('admin_products'))
    return render_template('admin/product_form.html', product=product)

@app.route('/admin/produto/salvar', methods=['POST'])
@admin_required
def admin_save_product():
    """Salva produto com múltiplas imagens e preços promocionais"""
    data = load_data()
    
    # Pega dados do formulário
    product_id = request.form.get('id') or str(uuid.uuid4())
    product_name = request.form.get('name')
    
    # Preços
    regular_price = float(request.form.get('price', 0))
    promotional_price = request.form.get('promotional_price')
    promotional_price = float(promotional_price) if promotional_price and promotional_price.strip() else None
    promotion_active = request.form.get('promotion_active') == 'on'
    
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
        'price': regular_price,
        'promotional_price': promotional_price,
        'promotion_active': promotion_active,
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
    
    # Mensagem com informação sobre promoção
    if promotion_active and promotional_price:
        discount_percent = calculate_discount_percentage(regular_price, promotional_price)
        flash(f'Produto "{product_name}" salvo com {discount_percent}% de desconto!', 'success')
    else:
        flash(f'Produto "{product_name}" salvo com sucesso!', 'success')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/produto/excluir/<product_id>')
@admin_required
def admin_product_delete(product_id):
    """Excluir produto"""
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

@app.route('/admin/anuncios')
@admin_required
def admin_announcements():
    """Gerenciar anúncios"""
    data = load_data()
    return render_template('admin/announcements.html', announcements=data.get('announcements', []))

@app.route('/admin/anuncio/novo')
@admin_required
def admin_new_announcement():
    """Novo anúncio"""
    return render_template('admin/announcement_form.html', announcement=None)

@app.route('/admin/anuncio/editar/<announcement_id>')
@admin_required
def admin_edit_announcement(announcement_id):
    """Editar anúncio"""
    data = load_data()
    announcement = next((a for a in data['announcements'] if a['id'] == announcement_id), None)
    
    if not announcement:
        flash('Anúncio não encontrado!', 'error')
        return redirect(url_for('admin_announcements'))
    
    return render_template('admin/announcement_form.html', announcement=announcement)

@app.route('/admin/anuncio/salvar', methods=['POST'])
@admin_required
def admin_save_announcement():
    """Salva anúncio com imagem"""
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

@app.route('/admin/anuncio/excluir/<announcement_id>')
@admin_required
def admin_delete_announcement(announcement_id):
    """Excluir anúncio"""
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