# Prima Arte - Estrutura CSS Modular

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
