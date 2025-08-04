
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
            content = content.replace('</div><!-- dashboard-grid -->', editor_card + '\n            </div><!-- dashboard-grid -->')
        elif '</div>' in content:
            # Se não houver o comentário, inserir antes do último </div> da seção
            last_div_pos = content.rfind('</div>')
            if last_div_pos != -1:
                content = content[:last_div_pos] + editor_card + '\n        ' + content[last_div_pos:]
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(content)

# Executar adição do link
add_editor_link_to_dashboard()
