const SCRIPT_URL = '/signup';

const form = document.getElementById('signup-form');
const status = document.getElementById('status');

form.addEventListener('submit', e => {
    e.preventDefault();
    
    const submitBtn = form.querySelector('button');
    submitBtn.disabled = true;
    submitBtn.innerText = 'Sending...';
    
    status.style.display = 'block';
    status.className = 'status-msg';
    status.innerText = 'Processing your request...';

    const formData = new FormData(form);
    
    fetch(SCRIPT_URL, { 
        method: 'POST', 
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        status.innerText = 'Success! You are on the waitlist.';
        status.className = 'status-msg success';
        form.reset();
        submitBtn.innerText = 'Join Waitlist';
        submitBtn.disabled = false;
    })
    .catch(error => {
        status.innerText = 'Oops! Error connecting to server. Make sure app.py is running.';
        status.className = 'status-msg error';
        submitBtn.innerText = 'Join Waitlist';
        submitBtn.disabled = false;
        console.error('Error!', error.message);
    });
});
