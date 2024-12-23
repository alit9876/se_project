const searchInput = document.getElementById('search-input');
        const suggestionsList = document.getElementById('suggestions-list');
        let suggestions = []; // Store suggestions here
    
        searchInput.addEventListener('input', function () {
            const query = this.value;
    
            if (query.length > 1) {
                fetch(`/search/suggestions/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestions = data.results;
                        suggestionsList.innerHTML = ''; // Clear the suggestions list
    
                        if (suggestions.length > 0) {
                            // Only show the first suggestion
                            suggestionsList.style.display = 'block';
                            const [name, url] = suggestions[0]; // Get the first suggestion
                            const listItem = document.createElement('li');
                            listItem.textContent = name;
                            listItem.style.cursor = 'pointer';
                            listItem.style.padding = '5px';
                            listItem.addEventListener('click', () => {
                                window.location.href = `/${url}`; // Redirect to the first suggestion
                            });
                            suggestionsList.appendChild(listItem);
                        } else {
                            suggestionsList.style.display = 'none'; // Hide the list if no suggestions
                        }
                    });
            } else {
                suggestionsList.style.display = 'none';
                suggestions = [];
            }
        });
    
        // Handle pressing Enter
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent form submission
                if (suggestions.length > 0) {
                    // Redirect to the first suggestion
                    window.location.href = `/${suggestions[0][1]}`;
                } else {
                    // Redirect to home if no suggestions
                    window.location.href = '/';
                }
            }
        });
    
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !suggestionsList.contains(e.target)) {
                suggestionsList.style.display = 'none';
            }
        });