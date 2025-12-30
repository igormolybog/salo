document.addEventListener('DOMContentLoaded', () => {
    // Click Tracking
    const trackClick = async (buttonId) => {
        // Track with Google Analytics (if ID is replaced)
        if (typeof gtag === 'function') {
            gtag('event', 'cta_click', {
                'button_id': buttonId
            });
        }
        
        try {
            await fetch('/track', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    event: 'cta_click',
                    metadata: { button_id: buttonId }
                }),
            });
        } catch (err) {
            console.error('Tracking failed', err);
        }
    };

    // Attach tracking to buttons
    const navBtn = document.getElementById('cta-nav');
    const heroBtn = document.getElementById('cta-hero');

    if (navBtn) {
        navBtn.addEventListener('click', () => trackClick('nav_get_access'));
    }
    if (heroBtn) {
        heroBtn.addEventListener('click', () => trackClick('hero_add_to_slack'));
    }

    // Form Handling (for signup.html)
    const signupForm = document.getElementById('signup-form');
    const formPanel = document.getElementById('form-panel');
    const successPanel = document.getElementById('success-panel');
    const loader = document.getElementById('loader');

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Show loader
            loader.style.display = 'block';
            
            const formData = new FormData(signupForm);
            
            try {
                const response = await fetch('/signup', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    formPanel.style.display = 'none';
                    successPanel.style.display = 'block';
                } else {
                    alert('Something went wrong. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Connection error. Please try again later.');
            } finally {
                loader.style.display = 'none';
            }
        });
    }
});
