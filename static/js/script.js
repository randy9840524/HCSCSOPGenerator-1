document.addEventListener('DOMContentLoaded', function() {
    // Generate Document ID when title changes
    const titleInput = document.getElementById('title');
    const documentIdInput = document.getElementById('document_id');

    titleInput.addEventListener('input', function() {
        // Generate UTC timestamp
        const timestamp = new Date().getTime();
        
        // Generate random components
        const random1 = Math.random().toString(36).substring(2, 6);
        const random2 = Math.random().toString(36).substring(2, 6);
        
        // Get clean prefix from title (max 3 chars)
        const prefix = this.value.trim()
            .substring(0, 3)
            .toUpperCase()
            .replace(/[^A-Z0-9]/g, 'X');
            
        // Create document ID with format: PREFIX-TIMESTAMP-RANDOM1-RANDOM2
        const docId = `${prefix}-${timestamp}-${random1}-${random2}`.toUpperCase();
        documentIdInput.value = docId;
        
        // Log the generated ID for debugging
        console.log('Generated Document ID:', documentIdInput.value);
    });

    // Form validation
    const form = document.getElementById('sopForm');
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });

    // Set minimum date for effective date
    const effectiveDateInput = document.getElementById('effective_date');
    const today = new Date().toISOString().split('T')[0];
    effectiveDateInput.setAttribute('min', today);
    
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
        });
    });
});
