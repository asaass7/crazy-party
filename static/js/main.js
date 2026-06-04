// Главный JavaScript файл

// Тёмная тема
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
        themeToggle.textContent = '☀️';
    }
    
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        const isDark = document.body.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        themeToggle.textContent = isDark ? '☀️' : '🌙';
    });
}

// Кнопка наверх
const scrollTopBtn = document.getElementById('scrollTopBtn');
if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollTopBtn.style.display = 'block';
        } else {
            scrollTopBtn.style.display = 'none';
        }
    });
    
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Авто-скрытие flash сообщений
setTimeout(() => {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 3000);
    });
}, 100);

// Аккордеон
document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
        const content = header.nextElementSibling;
        content.classList.toggle('active');
        
        // Закрываем другие
        document.querySelectorAll('.accordion-content').forEach(c => {
            if (c !== content) {
                c.classList.remove('active');
            }
        });
    });
});

// Анимация при скролле
const fadeElements = document.querySelectorAll('.fade-on-scroll');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.2 });

fadeElements.forEach(el => observer.observe(el));

// Маска для телефона
function phoneMask(input) {
    input.addEventListener('input', (e) => {
        let val = e.target.value.replace(/\D/g, '');
        if (val.length > 11) val = val.slice(0, 11);
        let formatted = '';
        if (val.length > 0) formatted = '+7';
        if (val.length > 1) formatted += ' (' + val.slice(1, 4);
        if (val.length >= 5) formatted += ') ' + val.slice(4, 7);
        if (val.length >= 8) formatted += '-' + val.slice(7, 9);
        if (val.length >= 10) formatted += '-' + val.slice(9, 11);
        e.target.value = formatted;
    });
}

// Применяем маску ко всем полям телефона
document.querySelectorAll('input[type="tel"]').forEach(phoneMask);// Version 1.0 - Main JavaScript file
