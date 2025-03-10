document.addEventListener('DOMContentLoaded', function() {
    const checkButton = document.getElementById('checkButton');
    const resultContainer = document.getElementById('result');
    const errorElement = document.getElementById('error');
    const spinner = checkButton.querySelector('.spinner');

    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    const root = document.documentElement;

    function getCurrentTheme() {
        return root.getAttribute('data-theme') || 'light';
    }

    function initializeTheme() {
        const savedTheme = localStorage.getItem('appTheme') || 'light';
        root.setAttribute('data-theme', savedTheme);
    }

    themeToggle.addEventListener('click', () => {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        root.setAttribute('data-theme', newTheme);
        localStorage.setItem('appTheme', newTheme);
        updateThemeToggleIcon(newTheme);
    });

    function updateThemeToggleIcon(theme) {
        const icon = themeToggle.querySelector('.theme-icon');
        icon.innerHTML = theme === 'light' 
            ? '<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>' // moon icon
            : '<circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>'; // sun icon
    }

    initializeTheme();
    updateThemeToggleIcon(getCurrentTheme());

    // Validate URL format
    function isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }

    // Check button event listener
    checkButton.addEventListener('click', function() {
        // Reset previous state
        resultContainer.textContent = '';
        resultContainer.classList.add('hidden');
        errorElement.classList.add('hidden');
        checkButton.disabled = true;
        spinner.classList.remove('hidden');

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            let currentTab = tabs[0];
            
            // Validate URL before sending
            if (!isValidUrl(currentTab.url)) {
                errorElement.textContent = 'Invalid URL: Please provide a valid web address';
                errorElement.classList.remove('hidden');
                spinner.classList.add('hidden');
                checkButton.disabled = false;
                return;
            }
            
            fetch('https://counteract-mitigation.onrender.com/check_app', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: currentTab.url})
            })
            .then(response => {
                if (!response.ok) {
                    // Handle HTTP errors
                    return response.json().then(errorData => {
                        throw new Error(errorData.details || 'Server Error');
                    });
                }
                return response.json();
            })
            .then(data => {
                // Clear any previous styles
                resultContainer.classList.remove('error', 'success');
                
                // Set result message and styling
                resultContainer.innerHTML = `<strong>${data.message}</strong>`;
                
                // Add detailed information
                if (data.details) {
                    resultContainer.innerHTML += `<br><small>${data.details}</small>`;
                }
                
                // Add domain age info if available
                if (data.domain_info && data.domain_info.age_info) {
                    const ageInfo = data.domain_info.age_info;
                    resultContainer.innerHTML += `
                        <br><small>
                        Domain: ${data.domain_info.domain}<br>
                        Creation Date: ${ageInfo.creation_date}<br>
                        Domain Age: ${ageInfo.age_days} days<br>
                        Registrar: ${ageInfo.registrar}
                        </small>`;
                }

                // Add legitimacy info if available
                if (data.legitimacy_info) {
                    resultContainer.innerHTML += `
                        <br><small>
                        Legitimacy: ${data.legitimacy_info.is_legitimate ? 'Legitimate' : 'Not Legitimate'}<br>
                        Details: ${data.legitimacy_info.details}
                        </small>`;
                }
                
                // Apply appropriate styling based on authenticity
                resultContainer.classList.add(data.is_fake ? 'error' : 'success');
                resultContainer.classList.remove('hidden');
            })
            .catch(error => {
                console.error('Verification Error:', error);
                errorElement.textContent = `Error: ${error.message || 'Unable to verify app authenticity'}`;
                errorElement.classList.remove('hidden');
            })
            .finally(() => {
                spinner.classList.add('hidden');
                checkButton.disabled = false;
            });
        });
    });
});