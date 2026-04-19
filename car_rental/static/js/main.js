// AutoLux — main.js

// Mobile nav toggle
function toggleNav() {
  const nav = document.getElementById('navMobile');
  nav.classList.toggle('open');
}

// Auto-dismiss alerts after 5 seconds
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.opacity = '0';
    alert.style.transform = 'translateX(20px)';
    alert.style.transition = 'all 0.4s ease';
    setTimeout(() => alert.remove(), 400);
  }, 5000);
});

// Booking: calculate price dynamically
const startDateInput = document.querySelector('[name="start_date"]');
const endDateInput = document.querySelector('[name="end_date"]');

if (startDateInput && endDateInput) {
  function calcPrice() {
    const start = new Date(startDateInput.value);
    const end = new Date(endDateInput.value);
    if (start && end && end > start) {
      const days = Math.max(1, Math.ceil((end - start) / (1000 * 60 * 60 * 24)));
      const priceEl = document.querySelector('.price-amount');
      const rateEl = document.querySelector('[data-day-rate]');
      if (priceEl && rateEl) {
        const rate = parseFloat(rateEl.dataset.dayRate);
        priceEl.textContent = (days * rate).toFixed(2) + ' DT';
      }
      // Show duration hint
      let hint = document.getElementById('duration-hint');
      if (!hint) {
        hint = document.createElement('p');
        hint.id = 'duration-hint';
        hint.style.cssText = 'font-size:0.8rem; color:#d4af37; margin-top:4px;';
        endDateInput.parentElement.appendChild(hint);
      }
      hint.textContent = `Durée : ${days} jour${days > 1 ? 's' : ''}`;
    }
  }
  startDateInput.addEventListener('change', calcPrice);
  endDateInput.addEventListener('change', calcPrice);

  // Set min date to today
  const today = new Date().toISOString().split('T')[0];
  startDateInput.min = today;
  endDateInput.min = today;
  startDateInput.addEventListener('change', () => { endDateInput.min = startDateInput.value; });
}

// Smooth scroll for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// Intersection Observer for animation
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.car-card, .feature-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});
