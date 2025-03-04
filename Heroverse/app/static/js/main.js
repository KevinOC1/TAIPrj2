// JavaScript principal para HeroVerse Comics

document.addEventListener('DOMContentLoaded', function() {
    // Resaltar el elemento activo en la barra lateral
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar a');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentLocation.includes(linkPath) && linkPath !== '/') {
            link.parentElement.classList.add('active');
            link.style.fontWeight = 'bold';
            link.style.borderLeftColor = '#d32f2f';
            link.style.backgroundColor = '#f0d0b0';
        }
    });
    
    // Otras funcionalidades JavaScript se pueden agregar aquí
});