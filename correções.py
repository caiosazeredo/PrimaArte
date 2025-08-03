#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 PRIMA ARTE - SCRIPT DE ATUALIZAÇÃO COMPLETO
==============================================
Aplica todas as correções solicitadas de uma vez
"""

import os
import re

def create_slug_function():
    """Função para criar slugs amigáveis"""
    return '''
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
'''

def update_app_py():
    """Atualiza o arquivo app.py com todas as correções"""
    
    # Lê o arquivo atual
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adiciona import urllib.parse se não existir
    if 'import urllib.parse' not in content:
        content = content.replace('import uuid', 'import uuid\nimport urllib.parse')
    
    # Adiciona função create_slug após os imports
    slug_function = create_slug_function()
    if 'def create_slug(' not in content:
        # Encontra onde inserir (após as configurações)
        insert_pos = content.find('DATA_FILE = \'data.json\'')
        if insert_pos != -1:
            insert_pos = content.find('\n', insert_pos) + 1
            content = content[:insert_pos] + slug_function + '\n' + content[insert_pos:]
    
    # Substitui a função cart
    cart_function = '''@app.route('/carrinho')
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
    
    return render_template('cart.html', cart_items=detailed_cart, total=total)'''
    
    # Substitui função cart existente
    cart_pattern = r'@app\.route\(\'/carrinho\'\).*?return render_template\(\'cart\.html\'.*?\)'
    content = re.sub(cart_pattern, cart_function, content, flags=re.DOTALL)
    
    # Substitui a rota do produto
    product_function = '''@app.route('/produto/<product_slug>')
def product_detail(product_slug):
    """Detalhes do produto com slug amigável"""
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
    
    return render_template('product.html', product=product)'''
    
    # Substitui função product_detail existente
    product_pattern = r'@app\.route\(\'/produto/<.*?>\'\).*?return render_template\(\'product\.html\'.*?\)'
    content = re.sub(product_pattern, product_function, content, flags=re.DOTALL)
    
    # Substitui a função checkout para corrigir WhatsApp
    checkout_function = '''@app.route('/finalizar-pedido')
def checkout():
    """Redireciona para WhatsApp com detalhes do pedido"""
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Seu carrinho está vazio!', 'error')
        return redirect(url_for('cart'))
    
    data = load_data()
    
    # Monta mensagem para WhatsApp (SEM escape de caracteres)
    message = "*🎨 NOVO PEDIDO - PRIMA ARTE*\\n\\n"
    total = 0
    
    for item in cart_items:
        product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            total += item_total
            
            message += f"📦 *{product['name']}*\\n"
            message += f"   Quantidade: {item['quantity']}\\n"
            message += f"   Preço: R$ {product['price']:.2f}\\n"
            if item.get('description'):
                message += f"   Obs: {item['description']}\\n"
            message += f"   Subtotal: R$ {item_total:.2f}\\n\\n"
    
    message += f"💰 *TOTAL: R$ {total:.2f}*\\n\\n"
    message += "Olá! Gostaria de finalizar este pedido! 😊"
    
    # URL do WhatsApp com encoding correto
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '').replace(' ', '')}?text={urllib.parse.quote(message)}"
    
    # Limpa carrinho após enviar
    session['cart'] = []
    
    return redirect(whatsapp_url)'''
    
    # Substitui função checkout existente
    checkout_pattern = r'@app\.route\(\'/finalizar-pedido\'\).*?return redirect\(whatsapp_url\)'
    content = re.sub(checkout_pattern, checkout_function, content, flags=re.DOTALL)
    
    # Salva o arquivo atualizado
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ app.py atualizado com sucesso!")

def create_products_html():
    """Cria o arquivo products.html completo"""
    content = '''{% extends "base.html" %}

{% block title %}Produtos - Prima Arte{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <div class="section-header">
            <h1 class="section-title">Nossos Produtos</h1>
            <p class="section-subtitle">Artesanato feito à mão com muito amor e dedicação</p>
        </div>
        
        <!-- Filtros -->
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="display: inline-flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
                <a href="{{ url_for('products') }}" class="filter-btn {% if not current_category %}active{% endif %}">
                    <i class="fas fa-th-large"></i> Todos
                </a>
                <a href="{{ url_for('products', categoria='costura') }}" class="filter-btn {% if current_category == 'costura' %}active{% endif %}">
                    <i class="fas fa-cut"></i> Costura
                </a>
                <a href="{{ url_for('products', categoria='decoracao') }}" class="filter-btn {% if current_category == 'decoracao' %}active{% endif %}">
                    <i class="fas fa-home"></i> Decoração
                </a>
                <a href="{{ url_for('products', categoria='acessorios') }}" class="filter-btn {% if current_category == 'acessorios' %}active{% endif %}">
                    <i class="fas fa-gem"></i> Acessórios
                </a>
                <a href="{{ url_for('products', categoria='personalizados') }}" class="filter-btn {% if current_category == 'personalizados' %}active{% endif %}">
                    <i class="fas fa-magic"></i> Personalizados
                </a>
            </div>
        </div>
        
        {% if products %}
        <div class="products-grid">
            {% for product in products %}
            <div class="product-card" data-category="{{ product.category }}">
                {% if product.images and product.images|length > 0 %}
                <img src="{{ product.images[0] }}" alt="{{ product.name }}" class="product-image">
                {% else %}
                <div class="product-image no-image">
                    <i class="fas fa-image"></i>
                </div>
                {% endif %}
                
                {% if product.featured %}
                <div class="featured-badge">
                    <i class="fas fa-star"></i> Destaque
                </div>
                {% endif %}
                
                <div class="product-info">
                    <h3 class="product-title">{{ product.name }}</h3>
                    <p class="product-description">{{ product.description[:100] }}{% if product.description|length > 100 %}...{% endif %}</p>
                    <div class="product-price">R$ {{ "%.2f"|format(product.price) }}</div>
                    
                    <div class="product-actions">
                        <a href="{{ url_for('product_detail', product_slug=product.name|slug) }}" class="btn-product-view">
                            <i class="fas fa-eye"></i> Ver Detalhes
                        </a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-state">
            <i class="fas fa-box-open"></i>
            <h3>
                {% if current_category %}
                    Nenhum produto encontrado nesta categoria
                {% else %}
                    Nenhum produto cadastrado ainda
                {% endif %}
            </h3>
            <p>
                {% if current_category %}
                    Tente uma categoria diferente ou entre em contato conosco!
                {% else %}
                    Em breve teremos produtos incríveis aqui!
                {% endif %}
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 2rem;">
                {% if current_category %}
                <a href="{{ url_for('products') }}" class="btn-primary-large">
                    <i class="fas fa-th-large"></i> Ver Todos
                </a>
                {% endif %}
                <a href="https://wa.me/5521973108293" target="_blank" class="btn-secondary-large">
                    <i class="fab fa-whatsapp"></i> Fale Conosco
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</section>

<style>
/* Filtros */
.filter-btn {
    background: rgba(212, 175, 55, 0.1);
    color: var(--primary-gold);
    border: 2px solid rgba(212, 175, 55, 0.2);
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.filter-btn:hover {
    background: rgba(212, 175, 55, 0.2);
    border-color: rgba(212, 175, 55, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
}

.filter-btn.active {
    background: var(--gradient-main);
    color: white;
    border-color: transparent;
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

/* Botões dos produtos */
.btn-product-view {
    background: rgba(38, 198, 218, 0.1);
    color: var(--primary-teal);
    border: 2px solid rgba(38, 198, 218, 0.2);
    padding: 0.75rem 1.5rem;
    border-radius: 20px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
    justify-content: center;
}

.btn-product-view:hover {
    background: rgba(38, 198, 218, 0.2);
    border-color: rgba(38, 198, 218, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(38, 198, 218, 0.2);
}

@media (max-width: 768px) {
    .filter-btn {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }
}
</style>
{% endblock %}'''
    
    with open('templates/products.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ templates/products.html criado!")

def create_cart_html():
    """Cria o arquivo cart.html completo"""
    content = '''{% extends "base.html" %}

{% block title %}Carrinho - Prima Arte{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <div class="section-header">
            <h1 class="section-title">Meu Carrinho</h1>
            <p class="section-subtitle">Revise seus itens antes de finalizar o pedido</p>
        </div>
        
        {% if cart_items %}
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
            <!-- Itens do Carrinho -->
            <div class="cart-container">
                <h2 style="font-family: var(--font-heading); color: var(--dark-brown); margin-bottom: 1.5rem;">
                    <i class="fas fa-shopping-cart"></i> Itens do Pedido
                </h2>
                
                {% for item in cart_items %}
                <div class="cart-item">
                    {% if item.images and item.images|length > 0 %}
                    <img src="{{ item.images[0] }}" alt="{{ item.name }}" class="cart-item-image">
                    {% else %}
                    <div class="cart-item-image no-image">
                        <i class="fas fa-image"></i>
                    </div>
                    {% endif %}
                    
                    <div class="cart-item-info">
                        <h3 class="cart-item-name">{{ item.name }}</h3>
                        <p style="color: var(--gray); font-size: 0.9rem; margin-bottom: 0.5rem;">
                            Quantidade: <strong>{{ item.quantity }}</strong>
                        </p>
                        {% if item.description %}
                        <p style="color: var(--gray); font-size: 0.8rem; margin-bottom: 0.5rem;">
                            <strong>Obs:</strong> {{ item.description }}
                        </p>
                        {% endif %}
                        <div class="cart-item-price">R$ {{ "%.2f"|format(item.price) }} cada</div>
                    </div>
                    
                    <div style="text-align: right;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: var(--primary-pink); margin-bottom: 1rem;">
                            R$ {{ "%.2f"|format(item.total) }}
                        </div>
                        <a href="{{ url_for('remove_from_cart', product_id=item.id) }}" 
                           class="remove-btn" 
                           onclick="return confirm('Remover este item do carrinho?')">
                            <i class="fas fa-trash"></i>
                        </a>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Resumo do Pedido -->
            <div class="cart-summary">
                <h2 style="font-family: var(--font-heading); color: var(--dark-brown); margin-bottom: 1.5rem;">
                    <i class="fas fa-calculator"></i> Resumo do Pedido
                </h2>
                
                <div style="background: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--primary-beige);">
                        <span>Subtotal:</span>
                        <span>R$ {{ "%.2f"|format(total) }}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <span style="color: var(--gray); font-size: 0.9rem;">
                            <i class="fab fa-whatsapp"></i> Finalização via WhatsApp
                        </span>
                        <span style="color: var(--primary-teal); font-weight: 600;">GRÁTIS</span>
                    </div>
                    
                    <hr style="border: none; border-top: 2px solid var(--primary-gold); margin: 1rem 0;">
                    
                    <div class="cart-total">
                        <strong>TOTAL: R$ {{ "%.2f"|format(total) }}</strong>
                    </div>
                </div>
                
                <a href="{{ url_for('checkout') }}" class="btn-primary-large" style="width: 100%; margin-bottom: 1rem; text-align: center;">
                    <i class="fab fa-whatsapp"></i>
                    Finalizar via WhatsApp
                </a>
                
                <a href="{{ url_for('products') }}" class="btn-secondary-large" style="width: 100%; text-align: center;">
                    <i class="fas fa-arrow-left"></i>
                    Continuar Comprando
                </a>
                
                <div style="background: rgba(38, 198, 218, 0.1); padding: 1rem; border-radius: 10px; margin-top: 1.5rem; border-left: 4px solid var(--primary-teal);">
                    <h4 style="color: var(--primary-teal); margin-bottom: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Como Funciona?
                    </h4>
                    <p style="font-size: 0.9rem; color: var(--gray); margin: 0; line-height: 1.4;">
                        Ao finalizar, você será redirecionado para o WhatsApp com os detalhes do seu pedido. 
                        Conversaremos sobre forma de pagamento e entrega!
                    </p>
                </div>
            </div>
        </div>
        {% else %}
        <!-- Carrinho Vazio -->
        <div class="empty-state">
            <i class="fas fa-shopping-cart"></i>
            <h3>Seu carrinho está vazio</h3>
            <p>Que tal conhecer nossos produtos artesanais feitos com muito carinho?</p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 2rem;">
                <a href="{{ url_for('products') }}" class="btn-primary-large">
                    <i class="fas fa-box-open"></i> Ver Produtos
                </a>
                <a href="https://wa.me/5521973108293" target="_blank" class="btn-secondary-large">
                    <i class="fab fa-whatsapp"></i> Fale Conosco
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</section>

<style>
@media (max-width: 768px) {
    .container > div:first-child {
        grid-template-columns: 1fr !important;
    }
    
    .cart-summary {
        order: -1;
    }
    
    .cart-item {
        flex-direction: column;
        text-align: center;
        gap: 1rem;
    }
    
    .cart-item > div:last-child {
        text-align: center;
    }
}
</style>
{% endblock %}'''
    
    with open('templates/cart.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ templates/cart.html criado!")

def create_product_html():
    """Cria o arquivo product.html completo com zoom e modal"""
    content = '''{% extends "base.html" %}

{% block title %}{{ product.name }} - Prima Arte{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: start;">
            <!-- Galeria de Imagens -->
            <div>
                {% if product.images and product.images|length > 0 %}
                <div class="product-gallery">
                    <!-- Imagem Principal -->
                    <div class="main-image">
                        <img id="mainImage" src="{{ product.images[0] }}" alt="{{ product.name }}" 
                             style="width: 100%; height: 400px; object-fit: cover; border-radius: 15px; box-shadow: var(--shadow-medium); cursor: zoom-in; transition: transform 0.3s ease;"
                             onclick="openImageModal('{{ product.images[0] }}')"
                             onmouseover="this.style.transform='scale(1.05)'"
                             onmouseout="this.style.transform='scale(1)'">
                    </div>
                    
                    <!-- Miniaturas -->
                    {% if product.images|length > 1 %}
                    <div class="image-thumbnails" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 0.5rem; margin-top: 1rem;">
                        {% for image in product.images %}
                        <img src="{{ image }}" alt="{{ product.name }}" 
                             onclick="changeMainImage('{{ image }}')"
                             style="width: 100%; height: 80px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 2px solid transparent; transition: all 0.3s ease;"
                             onmouseover="this.style.borderColor='var(--primary-gold)'; this.style.transform='scale(1.1)'"
                             onmouseout="this.style.borderColor='transparent'; this.style.transform='scale(1)'">
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                {% else %}
                <div style="width: 100%; height: 400px; background: var(--gradient-main); border-radius: 15px; display: flex; align-items: center; justify-content: center; color: white; font-size: 6rem; box-shadow: var(--shadow-medium);">
                    <i class="fas fa-image"></i>
                </div>
                {% endif %}
            </div>
            
            <!-- Detalhes do Produto -->
            <div>
                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: var(--shadow-soft);">
                    {% if product.featured %}
                    <div style="background: var(--gradient-secondary); color: white; padding: 0.5rem 1rem; border-radius: 15px; display: inline-flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; font-size: 0.9rem; font-weight: 600;">
                        <i class="fas fa-star"></i> Produto em Destaque
                    </div>
                    {% endif %}
                    
                    <h1 style="font-family: var(--font-heading); font-size: 2.5rem; color: var(--dark-brown); margin-bottom: 1rem;">
                        {{ product.name }}
                    </h1>
                    
                    <div style="background: var(--gradient-main); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
                        <span style="font-size: 2rem; font-weight: 700;">R$ {{ "%.2f"|format(product.price) }}</span>
                    </div>
                    
                    <div style="margin-bottom: 2rem;">
                        <h3 style="font-family: var(--font-heading); color: var(--dark-brown); margin-bottom: 1rem;">
                            <i class="fas fa-info-circle"></i> Descrição
                        </h3>
                        <p style="line-height: 1.6; color: var(--gray);">{{ product.description }}</p>
                    </div>
                    
                    <div style="margin-bottom: 2rem;">
                        <h3 style="font-family: var(--font-heading); color: var(--dark-brown); margin-bottom: 1rem;">
                            <i class="fas fa-tag"></i> Categoria
                        </h3>
                        <span style="background: var(--primary-beige); color: var(--dark-brown); padding: 0.5rem 1rem; border-radius: 15px; font-weight: 600;">
                            {{ product.category.title() }}
                        </span>
                    </div>
                    
                    <!-- Formulário Adicionar ao Carrinho -->
                    <form action="{{ url_for('add_to_cart') }}" method="post" style="margin-bottom: 2rem;">
                        <input type="hidden" name="product_id" value="{{ product.id }}">
                        
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; font-weight: 600; color: var(--dark-brown); margin-bottom: 0.5rem;">
                                <i class="fas fa-sort-numeric-up"></i> Quantidade:
                            </label>
                            <input type="number" name="quantity" value="1" min="1" max="10" 
                                   style="width: 100px; padding: 0.5rem; border: 2px solid var(--primary-beige); border-radius: 10px; font-size: 1rem;">
                        </div>
                        
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; font-weight: 600; color: var(--dark-brown); margin-bottom: 0.5rem;">
                                <i class="fas fa-comment"></i> Observações (opcional):
                            </label>
                            <textarea name="description" rows="3" placeholder="Cor preferida, tamanho, personalizações..."
                                      style="width: 100%; padding: 0.75rem; border: 2px solid var(--primary-beige); border-radius: 10px; font-family: var(--font-body); resize: vertical;"></textarea>
                        </div>
                        
                        <button type="submit" class="btn-primary-large add-to-cart-btn" style="width: 100%;">
                            <i class="fas fa-shopping-cart"></i>
                            Adicionar ao Carrinho
                        </button>
                    </form>
                    
                    <!-- Botões de Ação -->
                    <div style="display: flex; gap: 1rem;">
                        <a href="https://wa.me/5521973108293?text=Olá! Tenho interesse no produto: {{ product.name }}" 
                           target="_blank" class="btn-secondary-large" style="flex: 1; text-align: center;">
                            <i class="fab fa-whatsapp"></i>
                            Falar no WhatsApp
                        </a>
                        <a href="{{ url_for('products') }}" class="btn-neutral" 
                           style="padding: 1rem; border-radius: 25px; text-decoration: none; text-align: center; display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-arrow-left"></i>
                            Voltar
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Informações Adicionais -->
        <div style="margin-top: 3rem;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: var(--shadow-soft); text-align: center;">
                    <i class="fas fa-hands" style="font-size: 3rem; color: var(--primary-gold); margin-bottom: 1rem;"></i>
                    <h3 style="font-family: var(--font-heading); color: var(--dark-brown); margin-bottom: 1rem;">100% Artesanal</h3>
                    <p style="color: var(--gray);">Cada peça é única e feita à mão com muito carinho e dedicação.</p>
                </div>
                
                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: var(--shadow-soft); text-align: center;">
                    <i class="fas fa-heart" style="font-size: 3rem; color: var(--primary-pink); margin-bottom: 1rem;"></i>
                    <h3 style="font-family: var(--font-heading); color: var(--dark-brown); margin-bottom: 1rem;">Feito com Amor</h3>
                    <p style="color: var(--gray);">Todo nosso trabalho é feito com amor e atenção aos detalhes.</p>
                </div>
                
                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: var(--shadow-soft); text-align: center;">
                    <i class="fab fa-whatsapp" style="font-size: 3rem; color: var(--primary-teal); margin-bottom: 1rem;"></i>
                    <h3 style="font-family: var(--font-heading); color: var(--dark-brown); margin-bottom: 1rem;">Pedidos via WhatsApp</h3>
                    <p style="color: var(--gray);">Finalize seu pedido facilmente pelo WhatsApp. Rápido e seguro!</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Modal para Zoom da Imagem -->
<div id="imageModal" class="image-modal" onclick="closeImageModal()">
    <span class="close-modal">&times;</span>
    <img class="modal-content" id="modalImage">
    <div class="modal-caption" id="modalCaption"></div>
</div>

<script>
function changeMainImage(imageUrl) {
    document.getElementById('mainImage').src = imageUrl;
    
    // Remove seleção de todas as miniaturas
    const thumbnails = document.querySelectorAll('.image-thumbnails img');
    thumbnails.forEach(img => {
        img.style.borderColor = 'transparent';
    });
    
    // Adiciona seleção na miniatura clicada
    event.target.style.borderColor = 'var(--primary-gold)';
}

function openImageModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const caption = document.getElementById('modalCaption');
    
    modal.style.display = 'block';
    modalImg.src = imageSrc;
    caption.innerHTML = '{{ product.name }} - Clique para fechar';
    
    // Previne scroll do body
    document.body.style.overflow = 'hidden';
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
    
    // Restaura scroll do body
    document.body.style.overflow = 'auto';
}

// Seleciona primeira miniatura por padrão
document.addEventListener('DOMContentLoaded', function() {
    const firstThumbnail = document.querySelector('.image-thumbnails img');
    if (firstThumbnail) {
        firstThumbnail.style.borderColor = 'var(--primary-gold)';
    }
    
    // Fechar modal com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeImageModal();
        }
    });
});
</script>

<style>
/* Modal da Imagem */
.image-modal {
    display: none;
    position: fixed;
    z-index: 9999;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.9);
    animation: fadeIn 0.3s ease;
}

.modal-content {
    margin: auto;
    display: block;
    max-width: 90%;
    max-height: 90%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 10px;
    box-shadow: 0 10px 50px rgba(0,0,0,0.5);
    animation: zoomIn 0.3s ease;
}

.close-modal {
    position: absolute;
    top: 20px;
    right: 35px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    z-index: 10000;
    transition: all 0.3s ease;
}

.close-modal:hover {
    color: var(--primary-gold);
    transform: scale(1.2);
}

.modal-caption {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    text-align: center;
    background: rgba(0,0,0,0.7);
    padding: 1rem 2rem;
    border-radius: 25px;
    font-size: 1.1rem;
    backdrop-filter: blur(10px);
}

@keyframes zoomIn {
    from { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
    to { transform: translate(-50%, -50%) scale(1); opacity: 1; }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@media (max-width: 768px) {
    .container > div:first-child {
        grid-template-columns: 1fr !important;
        gap: 2rem !important;
    }
    
    .container > div:first-child > div:last-child {
        order: -1;
    }
    
    .image-thumbnails {
        grid-template-columns: repeat(4, 1fr) !important;
    }
    
    .modal-content {
        max-width: 95%;
        max-height: 80%;
    }
    
    .close-modal {
        top: 10px;
        right: 20px;
        font-size: 30px;
    }
    
    .modal-caption {
        bottom: 10px;
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
    }
}
</style>
{% endblock %}'''
    
    with open('templates/product.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ templates/product.html criado!")

def update_base_html():
    """Atualiza o base.html para usar o logo.jpg"""
    try:
        with open('templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substitui o logo por imagem se existe logo.jpg
        if os.path.exists('static/images/logo.jpg'):
            logo_old = '''<div class="logo-circle">
                            <i class="fas fa-heart"></i>
                        </div>'''
            
            logo_new = '''<div class="logo-circle">
                            <img src="{{ url_for('static', filename='images/logo.jpg') }}" alt="Prima Arte" 
                                 style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
                        </div>'''
            
            content = content.replace(logo_old, logo_new)
            
            with open('templates/base.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Logo atualizado no base.html!")
        else:
            print("⚠️  Logo.jpg não encontrado em static/images/")
    except Exception as e:
        print(f"⚠️  Erro ao atualizar base.html: {e}")

def update_index_html():
    """Atualiza index.html para usar slugs"""
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substitui os links para usar slugs
        old_link = '''<a href="{{ url_for('product_detail', product_id=product.id) }}" class="btn btn-primary">'''
        new_link = '''<a href="{{ url_for('product_detail', product_slug=product.name|slug) }}" class="btn-product-view">'''
        
        content = content.replace(old_link, new_link)
        
        # Corrige o texto do botão se necessário
        content = content.replace('Ver Detalhes</a>', '<i class="fas fa-eye"></i> Ver Detalhes</a>')
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ index.html atualizado!")
    except Exception as e:
        print(f"⚠️  Erro ao atualizar index.html: {e}")

def main():
    """Executa todas as atualizações"""
    print("🎨 " + "="*60)
    print("   PRIMA ARTE - APLICANDO TODAS AS CORREÇÕES")
    print("="*60)
    print()
    
    print("🔧 Atualizando arquivos...")
    print()
    
    try:
        # 1. Atualiza app.py
        update_app_py()
        
        # 2. Cria templates atualizados
        create_products_html()
        create_cart_html()
        create_product_html()
        
        # 3. Atualiza templates existentes
        update_base_html()
        update_index_html()
        
        print()
        print("🎊 " + "="*60)
        print("   ✅ TODAS AS CORREÇÕES APLICADAS COM SUCESSO!")
        print("="*60)
        print()
        print("🚀 Mudanças aplicadas:")
        print("   ✅ URLs amigáveis com slugs")
        print("   ✅ Fotos aparecem no carrinho")
        print("   ✅ WhatsApp com texto limpo") 
        print("   ✅ Zoom nas imagens de produto")
        print("   ✅ Modal para ver imagem grande")
        print("   ✅ Logo.jpg integrado (se existir)")
        print()
        print("📱 Teste agora:")
        print("   • Adicione produtos ao carrinho")
        print("   • Veja as URLs amigáveis")
        print("   • Teste o zoom nas imagens")
        print("   • Finalize um pedido no WhatsApp")
        print()
        
    except Exception as e:
        print(f"❌ Erro durante a atualização: {e}")
        print("Verifique se todos os arquivos existem e tente novamente.")

if __name__ == "__main__":
    main()