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
        // This function is executed when the fetch request is successful.
        // 'response' contains the response from the server.
        // Here, we extract JSON data from the response.
        return response.json(); // This returns a promise
     })
    .then(data => {
        console.log('Success:', data);
        const images = data.images; // Extract the array of image URLs

        // Clear previous images
        const generatedImagesContainer = document.getElementById('generated-images-container');
        generatedImagesContainer.innerHTML = '';

        // Display the four largest-numbered images
        images.forEach(imageUrl => {
            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            imgElement.classList.add('img-fluid', 'generated-img', 'm-2');
            generatedImagesContainer.appendChild(imgElement);
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

