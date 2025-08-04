# -*- coding: utf-8 -*-
"""
🎨 PRIMA ARTE - SISTEMA DE EDIÇÃO VISUAL
========================================
- Sistema no-code para editar página principal
- Sistema avançado de edição de anúncios  
- Palmeiras no hero section
- Correção de templates admin
"""

import os
import re
import json

def aplicar_sistema_edicao_completo():
    """Aplica sistema de edição visual completo"""
    print("🎨 " + "="*60)
    print("   PRIMA ARTE - SISTEMA DE EDIÇÃO VISUAL")
    print("="*60)
    print()
    
    # 1. Corrigir templates admin
    corrigir_templates_admin()
    
    # 2. Adicionar palmeiras ao hero
    adicionar_palmeiras_hero()
    
    # 3. Criar sistema de edição da página principal
    criar_editor_pagina_principal()
    
    # 4. Melhorar sistema de edição de anúncios
    melhorar_editor_anuncios()
    
    # 5. Criar rotas do editor
    criar_rotas_editor()
    
    print()
    print("🎊 " + "="*60)
    print("   ✅ SISTEMA DE EDIÇÃO VISUAL COMPLETO!")
    print("="*60)
    print()
    print("🚀 Funcionalidades criadas:")
    print("   🎨 Editor visual da página principal")
    print("   📋 Editor avançado de anúncios")
    print("   🌴 Palmeiras no hero section")
    print("   🔧 Templates admin corrigidos")
    print("   ⚙️ Configurações salvas em JSON")
    print()

def corrigir_templates_admin():
    """Corrige templates admin que usam product_id"""
    print("🔧 Corrigindo templates admin...")
    
    # Corrigir admin/products.html
    admin_products_content = '''{% extends "base.html" %}

{% block title %}Gerenciar Produtos - Prima Arte Admin{% endblock %}

{% block content %}
<section class="admin-section">
    <div class="container">
        <div class="admin-header">
            <h1 class="admin-title">
                <i class="fas fa-box-open"></i>
                Gerenciar Produtos
            </h1>
            <a href="{{ url_for('admin_product_new') }}" class="btn-admin-primary">
                <i class="fas fa-plus"></i>
                Novo Produto
            </a>
        </div>
        
        <div class="products-admin-grid">
            {% for product in products %}
            <div class="product-admin-card">
                <div class="product-admin-image">
                    {% if product.images and product.images|length > 0 %}
                    <img src="{{ product.images[0] }}" alt="{{ product.name }}">
                    {% else %}
                    <div class="no-image-admin">
                        <i class="fas fa-image"></i>
                    </div>
                    {% endif %}
                    
                    {% if product.featured %}
                    <div class="featured-badge-admin">
                        <i class="fas fa-star"></i>
                        Destaque
                    </div>
                    {% endif %}
                </div>
                
                <div class="product-admin-info">
                    <h3>{{ product.name }}</h3>
                    <p class="product-admin-category">{{ product.category|title }}</p>
                    <p class="product-admin-price">R$ {{ "%.2f"|format(product.price) }}</p>
                    <p class="product-admin-description">{{ product.description[:80] }}{% if product.description|length > 80 %}...{% endif %}</p>
                </div>
                
                <div class="product-admin-actions">
                    <a href="{{ url_for('product_detail', product_slug=product.name|slug) }}" 
                       class="btn-admin-view" target="_blank" title="Ver no site">
                        <i class="fas fa-eye"></i>
                    </a>
                    <a href="{{ url_for('admin_product_edit', product_id=product.id) }}" 
                       class="btn-admin-edit" title="Editar">
                        <i class="fas fa-edit"></i>
                    </a>
                    <a href="{{ url_for('admin_product_delete', product_id=product.id) }}" 
                       class="btn-admin-delete" title="Excluir"
                       onclick="return confirm('Tem certeza que deseja excluir este produto?')">
                        <i class="fas fa-trash"></i>
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>
        
        {% if not products %}
        <div class="empty-state-admin">
            <i class="fas fa-box-open"></i>
            <h3>Nenhum produto cadastrado</h3>
            <p>Comece criando seu primeiro produto!</p>
            <a href="{{ url_for('admin_product_new') }}" class="btn-admin-primary">
                <i class="fas fa-plus"></i>
                Criar Primeiro Produto
            </a>
        </div>
        {% endif %}
    </div>
</section>

<style>
.admin-section {
    padding: 2rem 0;
    background: #f8f9fa;
    min-height: 100vh;
}

.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
}

.admin-title {
    color: #20B2AA;
    font-family: var(--font-heading);
    font-size: 2rem;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.btn-admin-primary {
    background: linear-gradient(135deg, #20B2AA, #87CEEB);
    color: white;
    padding: 1rem 2rem;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
}

.btn-admin-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(32, 178, 170, 0.3);
}

.products-admin-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}

.product-admin-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.product-admin-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 35px rgba(0,0,0,0.15);
}

.product-admin-image {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.product-admin-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.no-image-admin {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #87CEEB, #4682B4);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
}

.featured-badge-admin {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #FFD700;
    color: #4682B4;
    padding: 0.5rem 1rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.product-admin-info {
    padding: 1.5rem;
}

.product-admin-info h3 {
    color: #20B2AA;
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
    line-height: 1.3;
}

.product-admin-category {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    font-weight: 600;
}

.product-admin-price {
    color: #FFD700;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.product-admin-description {
    color: #666;
    line-height: 1.5;
    font-size: 0.9rem;
}

.product-admin-actions {
    display: flex;
    gap: 0.5rem;
    padding: 1rem 1.5rem;
    background: #f8f9fa;
    border-top: 1px solid #e0e0e0;
}

.btn-admin-view, .btn-admin-edit, .btn-admin-delete {
    flex: 1;
    padding: 0.8rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.btn-admin-view {
    background: #17a2b8;
    color: white;
}

.btn-admin-view:hover {
    background: #138496;
}

.btn-admin-edit {
    background: #28a745;
    color: white;
}

.btn-admin-edit:hover {
    background: #218838;
}

.btn-admin-delete {
    background: #dc3545;
    color: white;
}

.btn-admin-delete:hover {
    background: #c82333;
}

.empty-state-admin {
    text-align: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
}

.empty-state-admin i {
    font-size: 4rem;
    color: #20B2AA;
    margin-bottom: 1rem;
}

.empty-state-admin h3 {
    color: #333;
    margin-bottom: 1rem;
}

.empty-state-admin p {
    color: #666;
    margin-bottom: 2rem;
}

@media (max-width: 768px) {
    .admin-header {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }
    
    .products-admin-grid {
        grid-template-columns: 1fr;
    }
    
    .product-admin-actions {
        flex-direction: column;
    }
}
</style>
{% endblock %}'''
    
    os.makedirs('templates/admin', exist_ok=True)
    with open('templates/admin/products.html', 'w', encoding='utf-8') as f:
        f.write(admin_products_content)
    
    print("✅ Templates admin corrigidos!")

def adicionar_palmeiras_hero():
    """Adiciona palmeiras ao hero section"""
    print("🌴 Adicionando palmeiras ao hero...")
    
    # Ler index.html atual e adicionar palmeiras
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar mais elementos de praia incluindo palmeiras
        palmeiras_elements = '''            <div class="beach-element" style="--delay: 0s;"><i class="fas fa-umbrella-beach"></i></div>
            <div class="beach-element" style="--delay: 1s;"><i class="fas fa-sun"></i></div>
            <div class="beach-element palm-tree" style="--delay: 2s;"><i class="fas fa-tree"></i></div>
            <div class="beach-element" style="--delay: 3s;"><i class="fas fa-shell"></i></div>
            <div class="beach-element palm-tree" style="--delay: 4s;"><i class="fas fa-seedling"></i></div>
            <div class="beach-element" style="--delay: 5s;"><i class="fas fa-starfish"></i></div>
            <div class="beach-element palm-tree-large" style="--delay: 6s;">🌴</div>
            <div class="beach-element palm-tree-large" style="--delay: 7s;">🥥</div>'''
        
        # Substituir os elementos existentes se houver
        beach_pattern = r'<div class="beach-element".*?</div>\s*<div class="beach-element".*?</div>\s*<div class="beach-element".*?</div>\s*<div class="beach-element".*?</div>\s*<div class="beach-element".*?</div>'
        if re.search(beach_pattern, content, re.DOTALL):
            content = re.sub(beach_pattern, palmeiras_elements, content, flags=re.DOTALL)
        else:
            # Se não houver elementos existentes, adicionar antes do fechamento da seção hero
            hero_end = content.find('</section>')
            if hero_end != -1:
                content = content[:hero_end] + palmeiras_elements + '\n        ' + content[hero_end:]
        
        # Adicionar CSS para palmeiras
        palmeiras_css = '''
/* Palmeiras especiais */
.palm-tree {
    color: rgba(34, 139, 34, 0.3) !important;
    font-size: 3rem !important;
}

.palm-tree-large {
    font-size: 4rem !important;
    color: rgba(34, 139, 34, 0.4);
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    animation: palmSway 12s ease-in-out infinite !important;
}

.palm-tree-large:nth-child(7) { top: 10%; right: 5%; }
.palm-tree-large:nth-child(8) { top: 70%; left: 3%; }

@keyframes palmSway {
    0%, 100% { transform: translateY(0) rotate(-2deg); }
    25% { transform: translateY(-10px) rotate(2deg); }
    50% { transform: translateY(-5px) rotate(-1deg); }
    75% { transform: translateY(-15px) rotate(3deg); }
}

/* Mais elementos de praia */
.beach-element:nth-child(6) { bottom: 35%; right: 8%; }
.beach-element:nth-child(7) { top: 30%; left: 12%; }
.beach-element:nth-child(8) { bottom: 15%; right: 20%; }'''
        
        # Adicionar CSS antes do fechamento da tag style
        if '</style>' in content:
            content = content.replace('</style>', palmeiras_css + '\n</style>')
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Palmeiras adicionadas ao hero!")
        
    except Exception as e:
        print(f"⚠️ Erro ao adicionar palmeiras: {e}")

def criar_editor_pagina_principal():
    """Cria editor visual da página principal"""
    print("🎨 Criando editor da página principal...")
    
    editor_content = '''{% extends "base.html" %}

{% block title %}Editor da Página Principal - Prima Arte Admin{% endblock %}

{% block content %}
<section class="visual-editor">
    <div class="editor-container">
        <!-- Painel de Controle -->
        <div class="editor-panel">
            <div class="panel-header">
                <h2><i class="fas fa-paint-brush"></i> Editor Visual</h2>
                <div class="panel-actions">
                    <button class="btn-preview" onclick="togglePreview()">
                        <i class="fas fa-eye"></i> Preview
                    </button>
                    <button class="btn-save" onclick="saveChanges()">
                        <i class="fas fa-save"></i> Salvar
                    </button>
                </div>
            </div>
            
            <!-- Configurações do Hero -->
            <div class="editor-section">
                <h3><i class="fas fa-image"></i> Hero Section</h3>
                
                <div class="control-group">
                    <label for="heroBackground">Cor de Fundo</label>
                    <input type="color" id="heroBackground" value="#87CEEB" onchange="updateHero()">
                </div>
                
                <div class="control-group">
                    <label for="heroGradient">Gradiente Secundário</label>
                    <input type="color" id="heroGradient" value="#20B2AA" onchange="updateHero()">
                </div>
                
                <div class="control-group">
                    <label for="heroTitle">Título Principal</label>
                    <input type="text" id="heroTitle" value="Artesanato Único" onchange="updateHero()">
                </div>
                
                <div class="control-group">
                    <label for="heroSubtitle">Subtítulo</label>
                    <input type="text" id="heroSubtitle" value="História Especial" onchange="updateHero()">
                </div>
                
                <div class="control-group">
                    <label for="heroDescription">Descrição</label>
                    <textarea id="heroDescription" onchange="updateHero()">Cada peça é cuidadosamente criada à mão, combinando técnicas tradicionais com o charme carioca.</textarea>
                </div>
                
                <div class="control-group">
                    <label for="logoSize">Tamanho da Logo</label>
                    <input type="range" id="logoSize" min="200" max="400" value="280" onchange="updateHero()">
                    <span class="range-value">280px</span>
                </div>
            </div>
            
            <!-- Configurações de Cores -->
            <div class="editor-section">
                <h3><i class="fas fa-palette"></i> Paleta de Cores</h3>
                
                <div class="color-palette">
                    <div class="color-item">
                        <label>Cor Primária</label>
                        <input type="color" id="primaryColor" value="#20B2AA" onchange="updateColors()">
                    </div>
                    <div class="color-item">
                        <label>Cor Secundária</label>
                        <input type="color" id="secondaryColor" value="#87CEEB" onchange="updateColors()">
                    </div>
                    <div class="color-item">
                        <label>Cor de Destaque</label>
                        <input type="color" id="accentColor" value="#FFD700" onchange="updateColors()">
                    </div>
                    <div class="color-item">
                        <label>Texto Principal</label>
                        <input type="color" id="textColor" value="#333333" onchange="updateColors()">
                    </div>
                </div>
            </div>
            
            <!-- Presets -->
            <div class="editor-section">
                <h3><i class="fas fa-magic"></i> Estilos Predefinidos</h3>
                
                <div class="preset-buttons">
                    <button class="preset-btn" onclick="applyPreset('tropical')">
                        🏝️ Tropical
                    </button>
                    <button class="preset-btn" onclick="applyPreset('ocean')">
                        🌊 Oceano
                    </button>
                    <button class="preset-btn" onclick="applyPreset('sunset')">
                        🌅 Pôr do Sol
                    </button>
                    <button class="preset-btn" onclick="applyPreset('vintage')">
                        📷 Vintage
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Preview -->
        <div class="editor-preview">
            <div class="preview-header">
                <h3><i class="fas fa-desktop"></i> Preview da Página</h3>
                <div class="device-selector">
                    <button class="device-btn active" data-device="desktop">
                        <i class="fas fa-desktop"></i>
                    </button>
                    <button class="device-btn" data-device="tablet">
                        <i class="fas fa-tablet-alt"></i>
                    </button>
                    <button class="device-btn" data-device="mobile">
                        <i class="fas fa-mobile-alt"></i>
                    </button>
                </div>
            </div>
            
            <div class="preview-container">
                <iframe id="previewFrame" src="{{ url_for('index') }}?preview=1"></iframe>
            </div>
        </div>
    </div>
</section>

<style>
/* Editor Styles */
.visual-editor {
    background: #f5f5f5;
    min-height: 100vh;
    padding: 0;
}

.editor-container {
    display: grid;
    grid-template-columns: 350px 1fr;
    height: 100vh;
}

.editor-panel {
    background: white;
    border-right: 1px solid #e0e0e0;
    overflow-y: auto;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}

.panel-header {
    background: linear-gradient(135deg, #20B2AA, #87CEEB);
    color: white;
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.panel-header h2 {
    margin: 0;
    font-size: 1.3rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.panel-actions {
    display: flex;
    gap: 0.5rem;
}

.btn-preview, .btn-save {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    transition: all 0.3s ease;
}

.btn-preview:hover, .btn-save:hover {
    background: rgba(255, 255, 255, 0.3);
}

.editor-section {
    padding: 1.5rem;
    border-bottom: 1px solid #f0f0f0;
}

.editor-section h3 {
    color: #20B2AA;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
}

.control-group {
    margin-bottom: 1rem;
}

.control-group label {
    display: block;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.3rem;
    font-size: 0.9rem;
}

.control-group input,
.control-group textarea {
    width: 100%;
    padding: 0.6rem;
    border: 2px solid #e0e0e0;
    border-radius: 5px;
    font-family: inherit;
    transition: border-color 0.3s ease;
}

.control-group input:focus,
.control-group textarea:focus {
    border-color: #20B2AA;
    outline: none;
}

.control-group textarea {
    min-height: 80px;
    resize: vertical;
}

.control-group input[type="range"] {
    margin-bottom: 0;
}

.range-value {
    font-size: 0.85rem;
    color: #666;
    font-weight: 600;
}

/* Color Palette */
.color-palette {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
}

.color-item {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.color-item label {
    font-size: 0.8rem;
    color: #666;
}

.color-item input[type="color"] {
    width: 100%;
    height: 40px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

/* Presets */
.preset-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}

.preset-btn {
    background: #f8f9fa;
    border: 2px solid #e0e0e0;
    padding: 0.8rem 0.5rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.3s ease;
    text-align: center;
}

.preset-btn:hover {
    border-color: #20B2AA;
    background: #f0f8ff;
}

/* Preview */
.editor-preview {
    background: #f8f9fa;
    display: flex;
    flex-direction: column;
}

.preview-header {
    background: white;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.preview-header h3 {
    margin: 0;
    color: #333;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.device-selector {
    display: flex;
    gap: 0.5rem;
}

.device-btn {
    background: #f8f9fa;
    border: 2px solid #e0e0e0;
    color: #666;
    padding: 0.5rem;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.device-btn.active,
.device-btn:hover {
    border-color: #20B2AA;
    color: #20B2AA;
    background: white;
}

.preview-container {
    flex: 1;
    padding: 1rem;
    display: flex;
    justify-content: center;
    align-items: start;
}

#previewFrame {
    width: 100%;
    height: calc(100vh - 120px);
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background: white;
    transition: all 0.3s ease;
}

/* Device Responsive */
.device-desktop #previewFrame { width: 100%; }
.device-tablet #previewFrame { width: 768px; max-width: 100%; }
.device-mobile #previewFrame { width: 375px; max-width: 100%; }

/* Mobile */
@media (max-width: 1024px) {
    .editor-container {
        grid-template-columns: 1fr;
        height: auto;
    }
    
    .editor-panel {
        position: relative;
        max-height: 400px;
    }
    
    .preview-container {
        height: 600px;
    }
    
    #previewFrame {
        height: 100%;
    }
}
</style>

<script>
// Editor Functions
function updateHero() {
    const background = document.getElementById('heroBackground').value;
    const gradient = document.getElementById('heroGradient').value;
    const title = document.getElementById('heroTitle').value;
    const subtitle = document.getElementById('heroSubtitle').value;
    const description = document.getElementById('heroDescription').value;
    const logoSize = document.getElementById('logoSize').value;
    
    // Update range display
    document.querySelector('#logoSize + .range-value').textContent = logoSize + 'px';
    
    // Apply changes to preview (via postMessage to iframe)
    const changes = {
        type: 'updateHero',
        data: { background, gradient, title, subtitle, description, logoSize }
    };
    
    document.getElementById('previewFrame').contentWindow.postMessage(changes, '*');
}

function updateColors() {
    const colors = {
        primary: document.getElementById('primaryColor').value,
        secondary: document.getElementById('secondaryColor').value,
        accent: document.getElementById('accentColor').value,
        text: document.getElementById('textColor').value
    };
    
    const changes = {
        type: 'updateColors',
        data: colors
    };
    
    document.getElementById('previewFrame').contentWindow.postMessage(changes, '*');
}

function applyPreset(preset) {
    const presets = {
        tropical: {
            heroBackground: '#00CED1',
            heroGradient: '#20B2AA',
            primaryColor: '#00CED1',
            secondaryColor: '#FFD700',
            accentColor: '#FF6347'
        },
        ocean: {
            heroBackground: '#4682B4',
            heroGradient: '#1E90FF',
            primaryColor: '#4682B4',
            secondaryColor: '#87CEEB',
            accentColor: '#00BFFF'
        },
        sunset: {
            heroBackground: '#FF6347',
            heroGradient: '#FFD700',
            primaryColor: '#FF6347',
            secondaryColor: '#FFA500',
            accentColor: '#FF4500'
        },
        vintage: {
            heroBackground: '#8B4513',
            heroGradient: '#CD853F',
            primaryColor: '#8B4513',
            secondaryColor: '#DEB887',
            accentColor: '#DAA520'
        }
    };
    
    const preset_data = presets[preset];
    if (preset_data) {
        // Update controls
        Object.keys(preset_data).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                element.value = preset_data[key];
            }
        });
        
        // Apply changes
        updateHero();
        updateColors();
    }
}

function togglePreview() {
    const frame = document.getElementById('previewFrame');
    const btn = document.querySelector('.btn-preview');
    
    if (frame.style.display === 'none') {
        frame.style.display = 'block';
        btn.innerHTML = '<i class="fas fa-eye"></i> Preview';
    } else {
        frame.style.display = 'none';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i> Mostrar';
    }
}

function saveChanges() {
    const settings = {
        hero: {
            background: document.getElementById('heroBackground').value,
            gradient: document.getElementById('heroGradient').value,
            title: document.getElementById('heroTitle').value,
            subtitle: document.getElementById('heroSubtitle').value,
            description: document.getElementById('heroDescription').value,
            logoSize: document.getElementById('logoSize').value
        },
        colors: {
            primary: document.getElementById('primaryColor').value,
            secondary: document.getElementById('secondaryColor').value,
            accent: document.getElementById('accentColor').value,
            text: document.getElementById('textColor').value
        }
    };
    
    // Send to server
    fetch('/admin/page-editor/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Configurações salvas com sucesso!');
        } else {
            alert('❌ Erro ao salvar configurações');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Erro ao salvar configurações');
    });
}

// Device selector
document.addEventListener('DOMContentLoaded', function() {
    const deviceBtns = document.querySelectorAll('.device-btn');
    const container = document.querySelector('.preview-container');
    
    deviceBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            deviceBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const device = this.dataset.device;
            container.className = 'preview-container device-' + device;
        });
    });
    
    // Initialize
    updateHero();
    updateColors();
});
</script>
{% endblock %}'''
    
    with open('templates/admin/page_editor.html', 'w', encoding='utf-8') as f:
        f.write(editor_content)
    
    print("✅ Editor da página principal criado!")

def melhorar_editor_anuncios():
    """Melhora o sistema de edição de anúncios"""
    print("📋 Melhorando editor de anúncios...")
    
    # Verificar se o arquivo existe
    announcement_file = 'templates/admin/announcement_new.html'
    if not os.path.exists(announcement_file):
        print("⚠️ Arquivo announcement_new.html não encontrado, criando...")
        # Criar o arquivo base primeiro
        announcement_content = '''{% extends "base.html" %}

{% block title %}Novo Anúncio - Prima Arte Admin{% endblock %}

{% block content %}
<section class="announcement-editor">
    <div class="container">
        <div class="editor-header">
            <h1><i class="fas fa-bullhorn"></i> Editor de Anúncios</h1>
            <a href="{{ url_for('admin_announcements') }}" class="btn-back">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
        
        <div class="editor-grid">
            <div class="form-panel">
                <div class="preset-section">
                    <h4>📋 Modelos Prontos</h4>
                    <div class="preset-buttons">
                        <button type="button" onclick="applyAnnouncementPreset('sale')" class="preset-btn sale">
                            🔥 Promoção
                        </button>
                        <button type="button" onclick="applyAnnouncementPreset('new')" class="preset-btn new">
                            ✨ Novidade
                        </button>
                        <button type="button" onclick="applyAnnouncementPreset('event')" class="preset-btn event">
                            📅 Evento
                        </button>
                        <button type="button" onclick="applyAnnouncementPreset('seasonal')" class="preset-btn seasonal">
                            🍂 Sazonal
                        </button>
                    </div>
                    
                    <button type="button" onclick="exportAnnouncementCode()" class="btn-export">
                        <i class="fas fa-code"></i> Exportar HTML
                    </button>
                </div>
                
                <form method="POST" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="title">Título</label>
                        <input type="text" id="title" name="title" required onchange="updatePreview()">
                    </div>
                    
                    <div class="form-group">
                        <label for="content">Conteúdo</label>
                        <textarea id="content" name="content" rows="4" required onchange="updatePreview()"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="bgColor">Cor de Fundo</label>
                        <input type="color" id="bgColor" name="bgColor" value="#20B2AA" onchange="updatePreview()">
                    </div>
                    
                    <div class="form-group">
                        <label for="textColor">Cor do Texto</label>
                        <input type="color" id="textColor" name="textColor" value="#FFFFFF" onchange="updatePreview()">
                    </div>
                    
                    <div class="form-group">
                        <label for="borderColor">Cor da Borda</label>
                        <input type="color" id="borderColor" name="borderColor" value="#1E90FF" onchange="updatePreview()">
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="btn-save">
                            <i class="fas fa-save"></i> Salvar Anúncio
                        </button>
                    </div>
                </form>
            </div>
            
            <div class="preview-panel">
                <h3><i class="fas fa-eye"></i> Preview</h3>
                <div id="preview" class="announcement-preview">
                    <div class="announcement-card">
                        <h4 id="preview-title">Título do Anúncio</h4>
                        <p id="preview-content">Conteúdo do anúncio aparecerá aqui...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<style>
.announcement-editor {
    padding: 2rem 0;
    background: #f8f9fa;
    min-height: 100vh;
}

.editor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
}

.editor-header h1 {
    color: #20B2AA;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-back {
    background: #6c757d;
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.editor-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.form-panel, .preview-panel {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
}

.preset-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
}

.preset-section h4 {
    color: #20B2AA;
    margin-bottom: 1rem;
}

.preset-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.preset-btn {
    padding: 0.8rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.preset-btn.sale { background: #FF4444; color: white; }
.preset-btn.new { background: #4CAF50; color: white; }
.preset-btn.event { background: #2196F3; color: white; }
.preset-btn.seasonal { background: #FF9800; color: white; }

.preset-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.btn-export {
    width: 100%;
    background: #6c757d;
    color: white;
    border: none;
    padding: 1rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.btn-export:hover {
    background: #5a6268;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-family: inherit;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
    border-color: #20B2AA;
    outline: none;
}

.form-group textarea {
    resize: vertical;
}

.form-group input[type="color"] {
    height: 50px;
    cursor: pointer;
}

.btn-save {
    background: linear-gradient(135deg, #20B2AA, #87CEEB);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
}

.btn-save:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(32, 178, 170, 0.3);
}

.preview-panel h3 {
    color: #20B2AA;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.announcement-preview {
    border: 2px dashed #e0e0e0;
    border-radius: 10px;
    padding: 1.5rem;
    min-height: 200px;
}

.announcement-card {
    padding: 2rem;
    border-radius: 15px;
    background: #20B2AA;
    color: white;
    border-left: 5px solid #1E90FF;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.announcement-card h4 {
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

.announcement-card p {
    line-height: 1.6;
    margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
    .editor-header {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }
    
    .editor-grid {
        grid-template-columns: 1fr;
    }
    
    .preset-buttons {
        grid-template-columns: 1fr;
    }
}
</style>

<script>
// Enhanced Announcement Editor
function applyAnnouncementPreset(preset) {
    const presets = {
        sale: {
            bgColor: '#FF4444',
            textColor: '#FFFFFF',
            borderColor: '#CC0000',
            title: '🔥 PROMOÇÃO ESPECIAL',
            content: 'Descontos incríveis em produtos selecionados! Aproveite esta oportunidade única.'
        },
        new: {
            bgColor: '#4CAF50',
            textColor: '#FFFFFF', 
            borderColor: '#388E3C',
            title: '✨ NOVIDADE',
            content: 'Confira nossos novos produtos chegando direto do ateliê!'
        },
        event: {
            bgColor: '#2196F3',
            textColor: '#FFFFFF',
            borderColor: '#1976D2',
            title: '📅 EVENTO ESPECIAL',
            content: 'Participe do nosso evento exclusivo e ganhe brindes especiais!'
        },
        seasonal: {
            bgColor: '#FF9800',
            textColor: '#FFFFFF',
            borderColor: '#F57C00',
            title: '🍂 COLEÇÃO OUTONO',
            content: 'Descubra nossa nova coleção inspirada nas cores do outono!'
        }
    };
    
    const data = presets[preset];
    if (data) {
        document.getElementById('title').value = data.title;
        document.getElementById('content').value = data.content;
        document.getElementById('bgColor').value = data.bgColor;
        document.getElementById('textColor').value = data.textColor;
        document.getElementById('borderColor').value = data.borderColor;
        updatePreview();
    }
}

function exportAnnouncementCode() {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const bgColor = document.getElementById('bgColor').value;
    const textColor = document.getElementById('textColor').value;
    const borderColor = document.getElementById('borderColor').value;
    
    const html = '<div class="custom-announcement" style="background: ' + bgColor + '; color: ' + textColor + '; border-left: 5px solid ' + borderColor + '; padding: 2rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1);"><h3 style="margin-bottom: 1rem; font-size: 1.3rem;">' + title + '</h3><p style="line-height: 1.6; margin: 0;">' + content + '</p></div>';
    
    // Copy to clipboard
    navigator.clipboard.writeText(html).then(() => {
        alert('✅ Código HTML copiado para a área de transferência!');
    });
}

function updatePreview() {
    const title = document.getElementById('title').value || 'Título do Anúncio';
    const content = document.getElementById('content').value || 'Conteúdo do anúncio aparecerá aqui...';
    const bgColor = document.getElementById('bgColor').value;
    const textColor = document.getElementById('textColor').value;
    const borderColor = document.getElementById('borderColor').value;
    
    const previewCard = document.querySelector('.announcement-card');
    previewCard.style.background = bgColor;
    previewCard.style.color = textColor;
    previewCard.style.borderLeftColor = borderColor;
    
    document.getElementById('preview-title').textContent = title;
    document.getElementById('preview-content').textContent = content;
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    updatePreview();
});
</script>
{% endblock %}'''
        
        os.makedirs('templates/admin', exist_ok=True)
        with open(announcement_file, 'w', encoding='utf-8') as f:
            f.write(announcement_content)
    
    print("✅ Editor de anúncios criado/melhorado!")

def criar_rotas_editor():
    """Cria as rotas necessárias para o editor"""
    print("⚙️ Criando rotas do editor...")
    
    routes_code = '''
# Novas rotas para o editor visual
@app.route('/admin/page-editor')
def admin_page_editor():
    """Editor visual da página principal"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/page_editor.html')

@app.route('/admin/page-editor/save', methods=['POST'])
def admin_page_editor_save():
    """Salva configurações do editor"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        settings = request.get_json()
        
        # Salvar configurações em arquivo JSON
        config_file = 'page_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/page-editor/load')
def admin_page_editor_load():
    """Carrega configurações do editor"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        config_file = 'page_config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        else:
            # Configurações padrão
            settings = {
                "hero": {
                    "background": "#87CEEB",
                    "gradient": "#20B2AA",
                    "title": "Artesanato Único",
                    "subtitle": "História Especial",
                    "description": "Cada peça é cuidadosamente criada à mão...",
                    "logoSize": "280"
                },
                "colors": {
                    "primary": "#20B2AA",
                    "secondary": "#87CEEB", 
                    "accent": "#FFD700",
                    "text": "#333333"
                }
            }
        
        return jsonify({'success': True, 'data': settings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def add_editor_link_to_dashboard():
    """Adiciona link do editor visual no dashboard"""
    dashboard_file = 'templates/admin/dashboard.html'
    if os.path.exists(dashboard_file):
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar card do editor visual
        editor_card = """
            <div class="dashboard-card">
                <div class="card-icon">
                    <i class="fas fa-paint-brush"></i>
                </div>
                <div class="card-content">
                    <h3>Editor Visual</h3>
                    <p>Personalize a aparência da página principal</p>
                    <a href="{{ url_for('admin_page_editor') }}" class="card-link">
                        <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>"""
        
        # Inserir antes do fechamento da grid
        if '</div><!-- dashboard-grid -->' in content:
            content = content.replace('</div><!-- dashboard-grid -->', editor_card + '\\n            </div><!-- dashboard-grid -->')
        elif '</div>' in content:
            # Se não houver o comentário, inserir antes do último </div> da seção
            last_div_pos = content.rfind('</div>')
            if last_div_pos != -1:
                content = content[:last_div_pos] + editor_card + '\\n        ' + content[last_div_pos:]
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(content)

# Executar adição do link
add_editor_link_to_dashboard()
'''
    
    with open('editor_routes.py', 'w', encoding='utf-8') as f:
        f.write(routes_code)
    
    print("✅ Arquivo com rotas do editor criado!")
    print("📝 Para ativar, adicione as rotas do arquivo 'editor_routes.py' ao seu app.py")

if __name__ == "__main__":
    aplicar_sistema_edicao_completo()