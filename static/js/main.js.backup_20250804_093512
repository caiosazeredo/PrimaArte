// Prima Arte - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Auto close flash messages
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(flash => {
        setTimeout(() => {
            if (flash.parentNode) {
                flash.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    if (flash.parentNode) {
                        flash.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
    
    // Add to cart animation
    const addToCartBtns = document.querySelectorAll('form[action*="adicionar-carrinho"] button');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Adicionado!';
            this.style.background = 'linear-gradient(135deg, #4CAF50, #45A049)';
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.background = '';
            }, 2000);
        });
    });
    
    console.log('🎨 Prima Arte - Site carregado!');
});

// CSS adicional
const additionalCSS = `
@keyframes slideOut {
    from {
        opacity: 1;
        transform: translateX(0);
    }
    to {
        opacity: 0;
        transform: translateX(100%);
    }
}
`;

const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);