function addPrompt(prompt) {
    var textarea = document.getElementById('suggested-prompt');
    if (textarea.value.length > 0) {
        textarea.value += ', ';
    }
    textarea.value += prompt;
}

document.getElementById('generate-btn').addEventListener('click', function() {
    var prompt = document.getElementById('suggested-prompt').value;

    // Make a POST request to the backend server
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        const images = data.images;

        // Clear previous images
        const generatedImagesContainer = document.getElementById('generated-images-container');
        generatedImagesContainer.innerHTML = '';

        // Display the images with a select button under each one
        images.forEach(imageUrl => {
            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            imgElement.classList.add('img-fluid', 'generated-img', 'm-2');

            const selectButton = document.createElement('button');
            selectButton.innerText = 'Select';
            selectButton.classList.add('btn', 'btn-primary', 'select-btn', 'm-2');
            selectButton.addEventListener('click', function() {
                // Deselect any previously selected image and button
                document.querySelectorAll('.selected-img').forEach(img => img.classList.remove('selected-img'));
                document.querySelectorAll('.btn-success').forEach(btn => btn.classList.replace('btn-success', 'btn-primary'));

                // Highlight the selected image and button
                imgElement.classList.add('selected-img');
                selectButton.classList.replace('btn-primary', 'btn-success');

                // Fill the selected image into the selected-image-frame
                const selectedImageFrame = document.getElementById('selected-image-frame');
                selectedImageFrame.innerHTML = ''; // Clear any previously selected image
                const selectedImage = document.createElement('img');
                selectedImage.src = imageUrl;
                selectedImage.classList.add('img-fluid');
                selectedImageFrame.appendChild(selectedImage);
            });

            generatedImagesContainer.appendChild(imgElement);
            generatedImagesContainer.appendChild(selectButton);
        });

        // Show confirm button after all images have been displayed
        document.getElementById('confirm-btn').style.display = 'block';
    })
    .catch(error => {
        console.error('Caught an error:', error);
    });
});

function selectGeneratedImage(imgElement) {
    // Deselect any previously selected image
    document.querySelectorAll('.generated-img').forEach(img => img.classList.remove('selected-img'));
    // Highlight the selected image
    imgElement.classList.add('selected-img');
    // Optionally, store the selected image URL or ID for further processing
}

