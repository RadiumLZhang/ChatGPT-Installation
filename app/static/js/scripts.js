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

document.getElementById('confirm-btn').addEventListener('click', function() {
    var prompt = document.getElementById('suggested-prompt').value;
    var selectedImage = document.querySelector('.selected-img').src;

    // Open the modal
    var modal = document.getElementById('creator-modal');
    modal.style.display = 'block';

    // Enable the submit button when the user enters their name
    document.getElementById('creator-name').addEventListener('input', function() {
        var submitBtn = document.getElementById('submit-btn');
        if (this.value) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    });

    // Save the data into the database when the form is submitted
    document.getElementById('creator-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var creatorName = document.getElementById('creator-name').value;
        var themeId = document.getElementById('theme-id').value;
        var prompt = document.getElementById('suggested-prompt').value;
        var selectedImage = document.querySelector('.selected-img').src;
        var content = document.getElementById('user-words').value;

        // TODO - Remove the hardcoded URL
        selectedImage = selectedImage.replace('http://127.0.0.1:8080/static/', '');
        // Make a POST request to the backend server
        fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt, image: selectedImage, creator: creatorName, theme_id: themeId, content: content}),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            modal.style.display = 'none';
            window.location.href = '/';  // Redirect to the main page
        })
        .catch(error => {
            console.error('Caught an error:', error);
        });
    });

    // Close the modal when the 'close-btn' is clicked
    document.getElementsByClassName('close-btn')[0].onclick = function() {
        modal.style.display = 'none';
    }

    // Close the modal when the user clicks outside of the modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});


$(document).ready(function() {
    // Add click event listener to each image
    $('.selectable-img').click(function() {
        // Remove border from all images
        $('.selectable-img').removeClass('selected-img');
        // Add border to clicked image
        $(this).addClass('selected-img');
    });
});
