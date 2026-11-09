document.addEventListener('DOMContentLoaded', () => {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : '';

    // Animated statistic counters
    const counters = document.querySelectorAll('.counter-value[data-target]');
    if (counters.length && 'IntersectionObserver' in window) {
        const animate = (el) => {
            const target = parseFloat(el.dataset.target) || 0;
            const isDecimal = el.dataset.decimal === 'true';
            const duration = 1400;
            const start = performance.now();
            const step = (now) => {
                const progress = Math.min((now - start) / duration, 1);
                const value = target * (1 - Math.pow(1 - progress, 3));
                el.textContent = isDecimal ? value.toFixed(1) : Math.round(value).toLocaleString('en-IN');
                if (progress < 1) requestAnimationFrame(step);
            };
            requestAnimationFrame(step);
        };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animate(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.4 });
        counters.forEach((c) => observer.observe(c));
    }

    // AJAX bookmark / save job toggle
    document.querySelectorAll('.btn-save-job-ajax').forEach((btn) => {
        btn.addEventListener('click', async (event) => {
            event.preventDefault();
            const jobId = btn.dataset.jobId;
            if (!jobId) return;
            btn.disabled = true;
            try {
                const res = await fetch(`/jobs/${jobId}/save`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    },
                    credentials: 'same-origin'
                });
                if (res.redirected || res.status === 401) {
                    window.location.href = '/auth/login';
                    return;
                }
                const data = await res.json();
                const icon = btn.querySelector('i.fa-bookmark');
                const label = btn.querySelector('.save-text');
                if (icon) {
                    icon.classList.toggle('fas', data.saved);
                    icon.classList.toggle('far', !data.saved);
                }
                if (label) label.textContent = data.saved ? 'Saved' : 'Save Job';
                if (btn.classList.contains('btn-cyan') || btn.classList.contains('btn-outline-cyan')) {
                    btn.classList.toggle('btn-cyan', data.saved);
                    btn.classList.toggle('btn-outline-cyan', !data.saved);
                }
                if (!data.saved && window.location.pathname.includes('saved-jobs')) {
                    const card = btn.closest('.col-lg-6');
                    if (card) card.remove();
                }
                showToast(data.message);
            } catch (err) {
                showToast('Could not update bookmark. Please sign in and try again.');
            } finally {
                btn.disabled = false;
            }
        });
    });

    // Auto-dismiss flash alerts
    document.querySelectorAll('.alert-dismissible').forEach((alert) => {
        setTimeout(() => {
            if (window.bootstrap) bootstrap.Alert.getOrCreateInstance(alert).close();
        }, 6000);
    });

    function showToast(message) {
        if (!message) return;
        const toast = document.createElement('div');
        toast.className = 'glass-card px-4 py-3 text-white small';
        toast.setAttribute('role', 'status');
        toast.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:2000;border:1px solid rgba(6,182,212,.4);';
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2600);
    }
});
