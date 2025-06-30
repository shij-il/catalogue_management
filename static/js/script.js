document.addEventListener('DOMContentLoaded', () => {
    const menuButtons = document.querySelectorAll('.menu-button');
    const formSections = document.querySelectorAll('.form-section');

    
    const catalogueForm = document.getElementById('catalogue-form');
    const nameInput = document.getElementById('name');
    const descriptionInput = document.getElementById('description');
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    const statusSelect = document.getElementById('status');
    const messageDiv = document.getElementById('message');

   
    const getCatalogueIdInput = document.getElementById('get-id');
    const fetchByIdBtn = document.getElementById('fetch-by-id-btn');
    const getCatalogueResultDiv = document.getElementById('get-catalogue-result');
    const getByIdMessageDiv = document.getElementById('get-id-message');

    
    const updateIdInput = document.getElementById('update-id');
    const fetchForUpdateBtn = document.getElementById('fetch-for-update-btn');
    const updateCatalogueForm = document.getElementById('update-catalogue-form');
    const updateNameInput = document.getElementById('update-name');
    const updateDescriptionInput = document.getElementById('update-description');
    const updateStartDateInput = document.getElementById('update-start_date');
    const updateEndDateInput = document.getElementById('update-end_date');
    const updateStatusSelect = document.getElementById('update-status');
    const updateMessageDiv = document.getElementById('update-message');

    
    const allCataloguesResultDiv = document.getElementById('all-catalogues-result');
    const allCataloguesMessageDiv = document.getElementById('all-catalogues-message');

    
    const deleteIdInput = document.getElementById('delete-id');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const deleteMessageDiv = document.getElementById('delete-message');


   
    const showSection = (id) => {
        formSections.forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(id).classList.add('active');
        clearAllMessages();
        clearAllResults();
    };

    
    const clearAllMessages = () => {
        const messageDivs = document.querySelectorAll('.message');
        messageDivs.forEach(div => {
            div.textContent = '';
            div.className = 'message'; 
        });
    };

   
    const clearAllResults = () => {
        getCatalogueResultDiv.innerHTML = '';
        allCataloguesResultDiv.innerHTML = '';
        updateCatalogueForm.style.display = 'none';
        
        catalogueForm.reset();
        getCatalogueIdInput.value = '';
        updateIdInput.value = '';
        deleteIdInput.value = '';
    };

    
    const displayMessage = (element, msg, type) => {
        element.textContent = msg;
        element.className = `message ${type}`; 
    };

    
    menuButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (button.id === 'exit-btn') {
                alert('Exiting... Goodbye!');
                
                return;
            }
            showSection(button.id.replace('-btn', '-form'));

            
            if (button.id === 'get-all-catalogues-btn') {
                fetchAllCatalogues();
            }
        });
    });

    
    showSection('create-catalogue-form');

    
    catalogueForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearAllMessages(); 

        const catalogueData = {
            name: nameInput.value,
            description: descriptionInput.value,
            start_date: startDateInput.value,
            end_date: endDateInput.value,
            status: statusSelect.value
        };

        
        for (const key in catalogueData) {
            if (!catalogueData[key]) {
                displayMessage(messageDiv, `Please fill in the ${key.replace('_', ' ')} field.`, 'error');
                return;
            }
        }

        try {
            const response = await fetch('/api/catalogues', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(catalogueData)
            });

            const data = await response.json();
            if (response.ok) {
                displayMessage(messageDiv, data.message, 'success');
                catalogueForm.reset(); 
            } else {
                displayMessage(messageDiv, `Error: ${data.error || 'Failed to create catalogue'}`, 'error');
            }
        } catch (error) {
            displayMessage(messageDiv, `Network error: ${error.message}. Please check if the backend server is running.`, 'error');
        }
    });

    
    fetchByIdBtn.addEventListener('click', async () => {
        clearAllMessages();
        getCatalogueResultDiv.innerHTML = ''; 

        const id = getCatalogueIdInput.value;
        if (!id) {
            displayMessage(getByIdMessageDiv, 'Please enter a Catalogue ID.', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/catalogues/${id}`);
            const data = await response.json();

            if (response.ok) {
                if (data.catalogue_id) { 
                    getCatalogueResultDiv.innerHTML = `
                        <div class="catalogue-item">
                            <p><strong>ID:</strong> ${data.catalogue_id}</p>
                            <p><strong>Name:</strong> ${data.name}</p>
                            <p><strong>Description:</strong> ${data.description}</p>
                            <p><strong>Start Date:</strong> ${data.start_date}</p>
                            <p><strong>End Date:</strong> ${data.end_date}</p>
                            <p><strong>Status:</strong> ${data.status}</p>
                        </div>
                    `;
                    displayMessage(getByIdMessageDiv, 'Catalogue found.', 'success');
                } else {
                    displayMessage(getByIdMessageDiv, data.message || 'Catalogue not found.', 'error');
                }
            } else {
                displayMessage(getByIdMessageDiv, `Error: ${data.error || 'Failed to fetch catalogue'}`, 'error');
            }
        } catch (error) {
            displayMessage(getByIdMessageDiv, `Network error: ${error.message}. Please check if the backend server is running.`, 'error');
        }
    });

   
    const fetchAllCatalogues = async () => {
        clearAllMessages();
        allCataloguesResultDiv.innerHTML = ''; 

        try {
            const response = await fetch('/api/catalogues');
            const data = await response.json();

            if (response.ok) {
                if (data.length > 0) {
                    data.forEach(catalogue => {
                        const catalogueItem = document.createElement('div');
                        catalogueItem.classList.add('catalogue-item');
                        catalogueItem.innerHTML = `
                            <p><strong>ID:</strong> ${catalogue.catalogue_id}</p>
                            <p><strong>Name:</strong> ${catalogue.name}</p>
                            <p><strong>Description:</strong> ${catalogue.description}</p>
                            <p><strong>Start Date:</strong> ${catalogue.start_date}</p>
                            <p><strong>End Date:</strong> ${catalogue.end_date}</p>
                            <p><strong>Status:</strong> ${catalogue.status}</p>
                        `;
                        allCataloguesResultDiv.appendChild(catalogueItem);
                    });
                    displayMessage(allCataloguesMessageDiv, `Successfully loaded ${data.length} catalogues.`, 'success');
                } else {
                    displayMessage(allCataloguesMessageDiv, 'No catalogues found.', 'success');
                }
            } else {
                displayMessage(allCataloguesMessageDiv, `Error: ${data.error || 'Failed to fetch catalogues'}`, 'error');
            }
        } catch (error) {
            displayMessage(allCataloguesMessageDiv, `Network error: ${error.message}. Please check if the backend server is running.`, 'error');
        }
    };

    
    fetchForUpdateBtn.addEventListener('click', async () => {
        clearAllMessages();
        updateCatalogueForm.style.display = 'none'; 

        const id = updateIdInput.value;
        if (!id) {
            displayMessage(updateMessageDiv, 'Please enter a Catalogue ID.', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/catalogues/${id}`);
            const data = await response.json();

            if (response.ok) {
                if (data.catalogue_id) {
                    updateNameInput.value = data.name;
                    updateDescriptionInput.value = data.description;
                    updateStartDateInput.value = data.start_date; 
                    updateEndDateInput.value = data.end_date;     
                    updateStatusSelect.value = data.status;
                    updateCatalogueForm.style.display = 'block'; 
                    displayMessage(updateMessageDiv, 'Catalogue details loaded. You can now update.', 'success');
                } else {
                    displayMessage(updateMessageDiv, data.message || 'Catalogue not found.', 'error');
                }
            } else {
                displayMessage(updateMessageDiv, `Error: ${data.error || 'Failed to fetch catalogue for update'}`, 'error');
            }
        } catch (error) {
            displayMessage(updateMessageDiv, `Network error: ${error.message}. Please check if the backend server is running.`, 'error');
        }
    });

    updateCatalogueForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearAllMessages();

        const id = updateIdInput.value; 
        const updatedData = {
            name: updateNameInput.value,
            description: updateDescriptionInput.value,
            start_date: updateStartDateInput.value,
            end_date: updateEndDateInput.value,
            status: updateStatusSelect.value
        };

        
        for (const key in updatedData) {
            if (!updatedData[key]) {
                displayMessage(updateMessageDiv, `Please fill in the ${key.replace('_', ' ')} field.`, 'error');
                return;
            }
        }

        try {
            const response = await fetch(`/api/catalogues/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedData)
            });

            const data = await response.json();
            if (response.ok) {
                displayMessage(updateMessageDiv, data.message, 'success');
                updateCatalogueForm.style.display = 'none'; 
                updateIdInput.value = ''; 
            } else {
                displayMessage(updateMessageDiv, `Error: ${data.error || 'Failed to update catalogue'}`, 'error');
            }
        } catch (error) {
            displayMessage(updateMessageDiv, `Network error: ${error.message}. Please check if the backend server is running.`, 'error');
        }
    });


    
    confirmDeleteBtn.addEventListener('click', async () => {
        clearAllMessages();
        const id = deleteIdInput.value;
        if (!id) {
            displayMessage(deleteMessageDiv, 'Please enter a Catalogue ID.', 'error');
            return;
        }

        if (!confirm(`Are you sure you want to delete catalogue with ID: ${id}? This action cannot be undone.`)) {
            return; // 
        }

        try {
            const response = await fetch(`/api/catalogues/${id}`, {
                method: 'DELETE'
            });

            const data = await response.json();
            if (response.ok) {
                displayMessage(deleteMessageDiv, data.message, 'success');
                deleteIdInput.value = ''; 
            } else {
                displayMessage(deleteMessageDiv, `Error: ${data.error || 'Failed to delete catalogue'}`, 'error');
            }
        } catch (error) {
            displayMessage(deleteMessageDiv, `Network error: ${error.message}. Please check if the backend server is running.`, 'error');
        }
    });
});