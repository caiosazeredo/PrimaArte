#!/usr/bin/env python3
"""
Script para remover todos os emojis das mensagens do WhatsApp

Este script:
1. Remove todos os emojis da mensagem de pedido
2. Mantém a formatação e estrutura
3. Deixa apenas texto limpo e profissional
"""

import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Faz backup de um arquivo antes de modificar"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_{timestamp}"
    shutil.copy2(filepath, backup_path)
    print(f"✅ Backup criado: {backup_path}")
    return backup_path

def remove_emojis_from_whatsapp_message():
    """Remove todos os emojis da mensagem do WhatsApp no app.py"""
    filepath = "app.py"
    
    if not os.path.exists(filepath):
        print(f"❌ Arquivo não encontrado: {filepath}")
        return False
    
    print(f"🔧 Removendo emojis da mensagem do WhatsApp: {filepath}")
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nova função checkout sem emojis
    new_checkout_function = '''@app.route('/finalizar-pedido')
def checkout():
    """Redireciona para WhatsApp com detalhes do pedido"""
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Seu carrinho está vazio!', 'error')
        return redirect(url_for('cart'))
    
    data = load_data()
    
    # Monta mensagem para WhatsApp com formatação limpa
    message = "*NOVO PEDIDO - PRIMA ARTE*\\n"
    message += "=" * 35 + "\\n\\n"
    
    total = 0
    item_count = 1
    
    for item in cart_items:
        product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            total += item_total
            
            message += f"*Item {item_count}:* {product['name']}\\n"
            message += f"   • Quantidade: {item['quantity']} unidade(s)\\n"
            message += f"   • Preço unitário: R$ {product['price']:.2f}\\n"
            
            if item.get('description'):
                message += f"   • Observações: {item['description']}\\n"
            
            message += f"   • Subtotal: *R$ {item_total:.2f}*\\n"
            message += "-" * 30 + "\\n"
            item_count += 1
    
    message += f"\\n*VALOR TOTAL: R$ {total:.2f}*\\n"
    message += "=" * 35 + "\\n\\n"
    message += "Olá! Gostaria de finalizar este pedido!\\n\\n"
    message += "*Próximos passos:*\\n"
    message += "• Confirmaremos os itens do pedido\\n"
    message += "• Combinaremos forma de pagamento\\n"
    message += "• Definiremos entrega/retirada\\n\\n"
    message += "Obrigado por escolher a Prima Arte!"
    
    # URL do WhatsApp com encoding correto
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '').replace(' ', '')}?text={urllib.parse.quote(message)}"
    
    # Limpa carrinho após enviar
    session['cart'] = []
    
    return redirect(whatsapp_url)'''

    # Encontra e substitui a função checkout
    import re
    
    # Procura pela função checkout
    pattern = r'@app\.route\(\'/finalizar-pedido\'\)\s*def checkout\(\):.*?return redirect\(whatsapp_url\)'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_checkout_function, content, flags=re.DOTALL)
        print("✅ Função checkout encontrada e atualizada!")
    else:
        print("⚠️  Função checkout não encontrada pelo regex. Tentando busca manual...")
        # Busca manual
        start_pos = content.find("@app.route('/finalizar-pedido')")
        if start_pos != -1:
            # Encontra próxima função ou final
            next_route = content.find("@app.route(", start_pos + 1)
            if next_route != -1:
                content = content[:start_pos] + new_checkout_function + '\n\n' + content[next_route:]
            else:
                # Se não encontrar próxima rota, procura por outras funções
                next_function = content.find("\ndef ", start_pos + 1)
                if next_function != -1:
                    content = content[:start_pos] + new_checkout_function + '\n\n' + content[next_function:]
                else:
                    content = content[:start_pos] + new_checkout_function + '\n\n'
            print("✅ Função checkout atualizada manualmente!")
        else:
            print("❌ Função checkout não encontrada!")
            return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filepath} atualizado com sucesso!")
    return True

def show_message_preview():
    """Mostra como ficará a nova mensagem"""
    print("\n📱 Preview da nova mensagem do WhatsApp:")
    print("=" * 50)
    
    preview_message = """*NOVO PEDIDO - PRIMA ARTE*
===================================

*Item 1:* Bolsa de Crochê Floral
   • Quantidade: 2 unidade(s)
   • Preço unitário: R$ 89.90
   • Subtotal: *R$ 179.80*
------------------------------

*VALOR TOTAL: R$ 179.80*
===================================

Olá! Gostaria de finalizar este pedido!

*Próximos passos:*
• Confirmaremos os itens do pedido
• Combinaremos forma de pagamento
• Definiremos entrega/retirada

Obrigado por escolher a Prima Arte!"""
    
    print(preview_message)
    print("=" * 50)

def main():
    """Função principal"""
    print("🚀 Removendo emojis das mensagens do WhatsApp...\n")
    
    success_count = 0
    
    # Remove emojis da mensagem
    try:
        if remove_emojis_from_whatsapp_message():
            success_count += 1
    except Exception as e:
        print(f"❌ Erro ao remover emojis: {e}")
    
    # Mostra preview da nova mensagem
    show_message_preview()
    
    print(f"\n🎉 Remoção de emojis concluída!")
    print(f"✅ {success_count} arquivo processado com sucesso")
    
    if success_count > 0:
        print(f"\n📝 Alterações realizadas:")
        print(f"   🗑️  Todos os emojis removidos da mensagem")
        print(f"   📱 Formatação limpa e profissional mantida")
        print(f"   ✨ Estrutura da mensagem preservada")
        print(f"\n✅ Nova mensagem:")
        print(f"   • Texto limpo sem emojis")
        print(f"   • Formatação profissional")
        print(f"   • Informações organizadas")
        print(f"   • Fácil de ler no WhatsApp")
        print(f"\n🔄 Próximos passos:")
        print(f"   1. Reinicie o servidor Flask")
        print(f"   2. Teste um pedido completo")
        print(f"   3. Verifique a mensagem no WhatsApp")

if __name__ == "__main__":
    main()