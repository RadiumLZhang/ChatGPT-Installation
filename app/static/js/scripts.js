function addPrompt(prompt) {
    var textarea = document.getElementById('suggested-prompt');
    if (textarea.value.length > 0) {
        textarea.value += ', ';
    }
    textarea.value += prompt;
}

document.getElementById('generate-btn').addEventListener('click', function() {
    // const promptText = document.getElementById('suggested-prompt').value; // Simulate using prompt text
    // const imagesGeneratedCount = 4; // Number of images to simulate generation for
    // const generatedImagesContainer = document.getElementById('generated-images-container');
    // generatedImagesContainer.innerHTML = ''; // Clear previous images
    //
    // // Simulate API response delay
    // setTimeout(() => {
    //     for (let i = 0; i < imagesGeneratedCount; i++) {
    //         // Simulate API response data
    //         const data = {
    //             imageUrl: '/static/images/image_generated.jpeg', // Path to your static test image
    //             imageId: `testImageId${i}` // Simulated unique ID for each image
    //         };
    //
    //         const imgElement = document.createElement('img');
    //         imgElement.src = data.imageUrl;
    //         imgElement.classList.add('img-fluid', 'generated-img', 'm-2');
    //         imgElement.setAttribute('data-img-id', data.imageId);
    //         imgElement.onclick = function() { selectGeneratedImage(this); };
    //         generatedImagesContainer.appendChild(imgElement);
    //
    //         if (i === imagesGeneratedCount - 1) {
    //             // Show confirm button after all images have been "generated" and displayed
    //             document.getElementById('confirm-btn').style.display = 'block';
    //         }
    //     }
    // }, 1000); // Adjust delay as needed to simulate network latency'

    var prompt = document.getElementById('suggested-prompt').value;

    // Make a POST request to the backend server
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        console.log(data.output); // Output of the Python script
        // Display the output or perform further actions as needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function selectGeneratedImage(imgElement) {
    // Deselect any previously selected image
    document.querySelectorAll('.generated-img').forEach(img => img.classList.remove('selected-img'));
    // Highlight the selected image
    imgElement.classList.add('selected-img');
    // Optionally, store the selected image URL or ID for further processing
}

