#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar referências CSS nos templates HTML
e organizar a estrutura CSS modular do Prima Arte
"""

import os
import re
from datetime import datetime

def backup_templates():
    """Cria backup de todos os templates"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    templates_dir = "templates"
    
    if not os.path.exists(templates_dir):
        print(f"❌ Diretório {templates_dir} não encontrado")
        return False
    
    backup_count = 0
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                backup_path = f"{file_path}.backup_{timestamp}"
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as original:
                        with open(backup_path, 'w', encoding='utf-8') as backup:
                            backup.write(original.read())
                    backup_count += 1
                except Exception as e:
                    print(f"❌ Erro ao fazer backup de {file_path}: {e}")
                    return False
    
    print(f"✅ {backup_count} templates com backup criado")
    return True

def create_css_structure():
    """Cria a estrutura de diretórios CSS"""
    css_dir = "static/css"
    
    # Criar diretório se não existir
    os.makedirs(css_dir, exist_ok=True)
    
    print(f"✅ Estrutura CSS criada em {css_dir}")
    return True

def update_base_template():
    """Atualiza o template base.html com as referências CSS corretas"""
    base_path = "templates/base.html"
    
    if not os.path.exists(base_path):
        print(f"❌ Template base não encontrado: {base_path}")
        return False
    
    try:
        with open(base_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Encontrar a seção de CSS
        css_pattern = r'<link rel="stylesheet" href="{{ url_for\(\'static\', filename=\'css/style\.css\'\) }}">'
        
        # Nova estrutura CSS modular
        new_css_links = '''<!-- CSS Principal -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    <!-- CSS Específico por Página -->
    {% block page_css %}{% endblock %}'''
        
        # Substituir a referência CSS única pela estrutura modular
        updated_content = re.sub(css_pattern, new_css_links, content)
        
        with open(base_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print("✅ Template base.html atualizado com estrutura CSS modular")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar base.html: {e}")
        return False

def update_index_template():
    """Atualiza o template index.html para usar home.css"""
    template_path = "templates/index.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template não encontrado: {template_path}")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Adicionar bloco page_css após {% extends "base.html" %}
        if '{% block page_css %}' not in content:
            extends_pattern = r'({% extends "base\.html" %})'
            css_block = '''{% extends "base.html" %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/home.css') }}">
{% endblock %}'''
            
            updated_content = re.sub(extends_pattern, css_block, content)
            
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print("✅ Template index.html atualizado com home.css")
        else:
            print("✅ Template index.html já possui bloco CSS")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar index.html: {e}")
        return False

def update_products_template():
    """Atualiza o template products.html para usar products.css"""
    template_path = "templates/products.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template não encontrado: {template_path}")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Adicionar bloco page_css após {% extends "base.html" %}
        if '{% block page_css %}' not in content:
            extends_pattern = r'({% extends "base\.html" %})'
            css_block = '''{% extends "base.html" %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/products.css') }}">
{% endblock %}'''
            
            updated_content = re.sub(extends_pattern, css_block, content)
            
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print("✅ Template products.html atualizado com products.css")
        else:
            print("✅ Template products.html já possui bloco CSS")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar products.html: {e}")
        return False

def update_product_detail_template():
    """Atualiza o template product.html para usar product-detail.css"""
    template_path = "templates/product.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template não encontrado: {template_path}")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Adicionar bloco page_css após {% extends "base.html" %}
        if '{% block page_css %}' not in content:
            extends_pattern = r'({% extends "base\.html" %})'
            css_block = '''{% extends "base.html" %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/product-detail.css') }}">
{% endblock %}'''
            
            updated_content = re.sub(extends_pattern, css_block, content)
            
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print("✅ Template product.html atualizado com product-detail.css")
        else:
            print("✅ Template product.html já possui bloco CSS")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar product.html: {e}")
        return False

def update_cart_template():
    """Atualiza o template cart.html para usar products.css (reutiliza estilos)"""
    template_path = "templates/cart.html"
    
    if not os.path.exists(template_path):
        print(f"⚠️ Template cart.html não encontrado - pulando")
        return True
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Adicionar bloco page_css após {% extends "base.html" %}
        if '{% block page_css %}' not in content:
            extends_pattern = r'({% extends "base\.html" %})'
            css_block = '''{% extends "base.html" %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/products.css') }}">
{% endblock %}'''
            
            updated_content = re.sub(extends_pattern, css_block, content)
            
            with open(template_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print("✅ Template cart.html atualizado com products.css")
        else:
            print("✅ Template cart.html já possui bloco CSS")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar cart.html: {e}")
        return False

def update_admin_templates():
    """Atualiza todos os templates administrativos para usar admin.css"""
    admin_templates = [
        "templates/admin/login.html",
        "templates/admin/dashboard.html", 
        "templates/admin/products.html",
        "templates/admin/product_form.html",
        "templates/admin/announcements.html",
        "templates/admin/announcement_form.html"
    ]
    
    updated_count = 0
    
    for template_path in admin_templates:
        if not os.path.exists(template_path):
            print(f"⚠️ Template admin não encontrado: {template_path} - pulando")
            continue
        
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Para login.html (não usa base.html)
            if 'login.html' in template_path:
                # Adicionar CSS diretamente no head
                if 'admin.css' not in content:
                    head_pattern = r'(<link rel="stylesheet" href="{{ url_for\(\'static\', filename=\'css/style\.css\'\) }}">[^<]*)'
                    css_replacement = '''<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/admin.css') }}">'''
                    
                    updated_content = re.sub(head_pattern, css_replacement, content)
                    
                    with open(template_path, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    
                    print(f"✅ Template {template_path} atualizado com admin.css")
                    updated_count += 1
                else:
                    print(f"✅ Template {template_path} já possui admin.css")
            
            # Para outros templates admin (usam base.html)
            else:
                if '{% block page_css %}' not in content:
                    extends_pattern = r'({% extends "base\.html" %})'
                    css_block = '''{% extends "base.html" %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/admin.css') }}">
{% endblock %}'''
                    
                    updated_content = re.sub(extends_pattern, css_block, content)
                    
                    with open(template_path, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    
                    print(f"✅ Template {template_path} atualizado com admin.css")
                    updated_count += 1
                else:
                    print(f"✅ Template {template_path} já possui bloco CSS")
        
        except Exception as e:
            print(f"❌ Erro ao atualizar {template_path}: {e}")
            continue
    
    print(f"✅ {updated_count} templates administrativos atualizados")
    return True

def fix_zoom_javascript():
    """Corrige o JavaScript do zoom no template product.html"""
    template_path = "templates/product.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template product.html não encontrado")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # JavaScript corrigido para o zoom
        fixed_js = '''
let currentImageIndex = 0;
let currentZoom = 1;
let minZoom = 0.5;
let maxZoom = 3;
let isDragging = false;
let startX, startY, startTransformX = 0, startTransformY = 0;

let productImages = [
    {% for image in product.images %}
    "{{ image }}"{% if not loop.last %},{% endif %}
    {% endfor %}
];

function changeMainImage(imageUrl, index) {
    document.getElementById('mainImage').src = imageUrl;
    currentImageIndex = index;
    
    // Remove active class from all thumbnails
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.classList.remove('active');
    });
    
    // Add active class to clicked thumbnail
    const thumbnail = document.querySelector(`[data-index="${index}"]`);
    if (thumbnail) {
        thumbnail.classList.add('active');
    }
}

function openImageModal(index = 0) {
    currentImageIndex = index;
    
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const counter = document.getElementById('imageCounter');
    
    modal.style.display = 'block';
    modalImg.src = productImages[currentImageIndex];
    counter.textContent = `${currentImageIndex + 1} / ${productImages.length}`;
    
    // CORREÇÃO: Iniciar sempre com zoom 100% (fit-to-container)
    currentZoom = 1;
    resetImagePosition();
    updateZoomLevel();
    updateModalThumbnails();
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    currentZoom = 1;
    resetImagePosition();
}

function nextImage() {
    if (currentImageIndex < productImages.length - 1) {
        currentImageIndex++;
    } else {
        currentImageIndex = 0;
    }
    updateModalImage();
}

function previousImage() {
    if (currentImageIndex > 0) {
        currentImageIndex--;
    } else {
        currentImageIndex = productImages.length - 1;
    }
    updateModalImage();
}

function goToImage(index) {
    currentImageIndex = index;
    updateModalImage();
}

function updateModalImage() {
    const modalImg = document.getElementById('modalImage');
    const counter = document.getElementById('imageCounter');
    
    modalImg.src = productImages[currentImageIndex];
    counter.textContent = `${currentImageIndex + 1} / ${productImages.length}`;
    
    // Reset zoom when changing images
    currentZoom = 1;
    resetImagePosition();
    updateModalThumbnails();
}

function updateModalThumbnails() {
    document.querySelectorAll('.modal-thumbnail').forEach((thumb, index) => {
        thumb.classList.toggle('active', index === currentImageIndex);
    });
}

// Funções de Zoom Corrigidas
function zoomIn() {
    if (currentZoom < maxZoom) {
        currentZoom = Math.min(currentZoom + 0.25, maxZoom);
        applyZoom();
    }
}

function zoomOut() {
    if (currentZoom > minZoom) {
        currentZoom = Math.max(currentZoom - 0.25, minZoom);
        applyZoom();
    }
}

function resetZoom() {
    currentZoom = 1;
    resetImagePosition();
    applyZoom();
}

function applyZoom() {
    const modalImg = document.getElementById('modalImage');
    const container = document.getElementById('imageContainer');
    
    // CORREÇÃO: Aplicar zoom corretamente
    modalImg.style.transform = `scale(${currentZoom}) translate(${startTransformX}px, ${startTransformY}px)`;
    updateZoomLevel();
    
    // Ajustar cursor baseado no zoom
    if (currentZoom > 1 && container) {
        container.style.cursor = 'grab';
    } else if (container) {
        container.style.cursor = 'default';
        // Reset position when zoom is 1 or less
        if (currentZoom <= 1) {
            resetImagePosition();
        }
    }
}

function resetImagePosition() {
    startTransformX = 0;
    startTransformY = 0;
    const modalImg = document.getElementById('modalImage');
    if (modalImg) {
        modalImg.style.transform = `scale(${currentZoom})`;
    }
}

function updateZoomLevel() {
    const zoomLevelElement = document.getElementById('zoomLevel');
    if (zoomLevelElement) {
        zoomLevelElement.textContent = `${Math.round(currentZoom * 100)}%`;
    }
}

function increaseQuantity() {
    const qty = document.getElementById('quantity');
    if (qty && parseInt(qty.value) < 10) {
        qty.value = parseInt(qty.value) + 1;
    }
}

function decreaseQuantity() {
    const qty = document.getElementById('quantity');
    if (qty && parseInt(qty.value) > 1) {
        qty.value = parseInt(qty.value) - 1;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Set first thumbnail as active
    const firstThumbnail = document.querySelector('.thumbnail');
    if (firstThumbnail) {
        firstThumbnail.classList.add('active');
    }
    
    // Modal drag functionality
    const imageContainer = document.getElementById('imageContainer');
    const modalImage = document.getElementById('modalImage');
    
    if (imageContainer && modalImage) {
        // Mouse events
        imageContainer.addEventListener('mousedown', startDrag);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', endDrag);
        
        // Touch events for mobile
        imageContainer.addEventListener('touchstart', startDragTouch, {passive: false});
        document.addEventListener('touchmove', dragTouch, {passive: false});
        document.addEventListener('touchend', endDrag);
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        const modal = document.getElementById('imageModal');
        if (modal && modal.style.display === 'block') {
            switch(e.key) {
                case 'Escape':
                    closeImageModal();
                    break;
                case 'ArrowLeft':
                    previousImage();
                    break;
                case 'ArrowRight':
                    nextImage();
                    break;
                case '+':
                case '=':
                    zoomIn();
                    break;
                case '-':
                    zoomOut();
                    break;
                case '0':
                    resetZoom();
                    break;
            }
        }
    });
    
    // Mouse wheel zoom
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.addEventListener('wheel', function(e) {
            if (e.target.closest('.modal-image-container')) {
                e.preventDefault();
                if (e.deltaY < 0) {
                    zoomIn();
                } else {
                    zoomOut();
                }
            }
        }, {passive: false});
        
        // Click outside modal to close
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeImageModal();
            }
        });
    }
});

// Drag functions
function startDrag(e) {
    if (currentZoom <= 1) return;
    
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    const container = document.getElementById('imageContainer');
    if (container) {
        container.style.cursor = 'grabbing';
    }
}

function startDragTouch(e) {
    if (currentZoom <= 1) return;
    
    isDragging = true;
    const touch = e.touches[0];
    startX = touch.clientX;
    startY = touch.clientY;
    e.preventDefault();
}

function drag(e) {
    if (!isDragging || currentZoom <= 1) return;
    
    e.preventDefault();
    const deltaX = e.clientX - startX;
    const deltaY = e.clientY - startY;
    
    startTransformX += deltaX;
    startTransformY += deltaY;
    
    const modalImg = document.getElementById('modalImage');
    if (modalImg) {
        modalImg.style.transform = `scale(${currentZoom}) translate(${startTransformX}px, ${startTransformY}px)`;
    }
    
    startX = e.clientX;
    startY = e.clientY;
}

function dragTouch(e) {
    if (!isDragging || currentZoom <= 1) return;
    
    e.preventDefault();
    const touch = e.touches[0];
    const deltaX = touch.clientX - startX;
    const deltaY = touch.clientY - startY;
    
    startTransformX += deltaX;
    startTransformY += deltaY;
    
    const modalImg = document.getElementById('modalImage');
    if (modalImg) {
        modalImg.style.transform = `scale(${currentZoom}) translate(${startTransformX}px, ${startTransformY}px)`;
    }
    
    startX = touch.clientX;
    startY = touch.clientY;
}

function endDrag() {
    isDragging = false;
    const container = document.getElementById('imageContainer');
    if (container && currentZoom > 1) {
        container.style.cursor = 'grab';
    }
}
'''
        
        # Substituir JavaScript existente
        js_pattern = r'<script>.*?</script>'
        new_js = f"<script>{fixed_js}\n</script>"
        
        updated_content = re.sub(js_pattern, new_js, content, flags=re.DOTALL)
        
        with open(template_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print("✅ JavaScript do zoom corrigido no product.html")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir JavaScript: {e}")
        return False

def create_readme():
    """Cria README com instruções da estrutura CSS"""
    readme_content = """# Prima Arte - Estrutura CSS Modular

## 📁 Estrutura de Arquivos CSS

```
static/css/
├── style.css           # Estilos gerais (header, footer, botões, formulários)
├── home.css            # Página inicial (hero, beach theme, produtos em destaque)
├── products.css        # Página de produtos (grid, filtros, cards)
├── product-detail.css  # Página individual do produto (galeria, zoom, formulário)
└── admin.css           # Área administrativa (dashboard, formulários, gerenciamento)
```

## 🎯 Como Funciona

### Template Base (base.html)
```html
<!-- CSS Principal -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

<!-- CSS Específico por Página -->
{% block page_css %}{% endblock %}
```

### Templates Específicos
Cada página adiciona seu CSS específico:

```html
{% extends "base.html" %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/home.css') }}">
{% endblock %}
```

## 📋 Mapeamento Template → CSS

| Template | CSS Usado |
|----------|-----------|
| `base.html` | `style.css` (sempre) |
| `index.html` | `style.css` + `home.css` |
| `products.html` | `style.css` + `products.css` |
| `product.html` | `style.css` + `product-detail.css` |
| `cart.html` | `style.css` + `products.css` |
| `admin/*.html` | `style.css` + `admin.css` |

## ✨ Vantagens

1. **Modular**: Cada página carrega apenas o CSS necessário
2. **Organizado**: Estilos separados por funcionalidade
3. **Performático**: Menos CSS desnecessário por página
4. **Manutenível**: Fácil de encontrar e editar estilos específicos
5. **Escalável**: Fácil adicionar novos estilos sem conflitos

## 🔧 Personalização

Para adicionar uma nova página:

1. Crie o arquivo CSS específico em `static/css/`
2. Adicione o bloco `{% block page_css %}` no template
3. Inclua a referência para o novo CSS

Exemplo:
```html
{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/minha-pagina.css') }}">
{% endblock %}
```
"""
    
    try:
        with open("CSS_README.md", 'w', encoding='utf-8') as file:
            file.write(readme_content)
        
        print("✅ README da estrutura CSS criado: CSS_README.md")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar README: {e}")
        return False

def main():
    """Função principal"""
    print("🎨 PRIMA ARTE - Atualização de Referências CSS Modulares")
    print("=" * 65)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script a partir da pasta raiz do projeto Prima Arte")
        return
    
    print("📋 Iniciando processo de atualização...")
    
    # 1. Criar backups
    print("\n1️⃣ Criando backups dos templates...")
    if not backup_templates():
        print("❌ Falha ao criar backups. Abortando.")
        return
    
    # 2. Criar estrutura CSS
    print("\n2️⃣ Criando estrutura de diretórios...")
    if not create_css_structure():
        print("❌ Falha ao criar estrutura CSS. Abortando.")
        return
    
    # 3. Atualizar template base
    print("\n3️⃣ Atualizando template base...")
    if not update_base_template():
        print("❌ Falha ao atualizar base.html. Abortando.")
        return
    
    # 4. Atualizar templates específicos
    print("\n4️⃣ Atualizando templates específicos...")
    update_index_template()
    update_products_template()
    update_product_detail_template()
    update_cart_template()
    
    # 5. Atualizar templates administrativos
    print("\n5️⃣ Atualizando templates administrativos...")
    update_admin_templates()
    
    # 6. Corrigir JavaScript do zoom
    print("\n6️⃣ Corrigindo JavaScript do zoom...")
    fix_zoom_javascript()
    
    # 7. Criar documentação
    print("\n7️⃣ Criando documentação...")
    create_readme()
    
    print("\n🎉 ATUALIZAÇÃO COMPLETA!")
    print("\n📋 Resumo das mudanças:")
    print("   ✅ Templates com backup criado")
    print("   ✅ Estrutura CSS modular implementada")
    print("   ✅ Template base.html atualizado")
    print("   ✅ Templates específicos atualizados:")
    print("      • index.html → home.css")
    print("      • products.html → products.css")
    print("      • product.html → product-detail.css")
    print("      • cart.html → products.css")
    print("   ✅ Templates administrativos → admin.css")
    print("   ✅ JavaScript do zoom corrigido")
    print("   ✅ Documentação criada (CSS_README.md)")
    
    print("\n📁 Arquivos CSS necessários:")
    print("   • static/css/style.css (estilos gerais)")
    print("   • static/css/home.css (página inicial)")
    print("   • static/css/products.css (página produtos)")
    print("   • static/css/product-detail.css (produto individual)")
    print("   • static/css/admin.css (área administrativa)")
    
    print("\n🔄 Próximos passos:")
    print("   1. Adicione os 5 arquivos CSS na pasta static/css/")
    print("   2. Reinicie o servidor Flask: python app.py")
    print("   3. Teste todas as páginas")
    print("   4. Ajuste estilos específicos se necessário")
    
    print("\n🎯 Resultado: CSS modular, organizado e sem conflitos!")

if __name__ == "__main__":
    main()