
document.getElementById('generate-btn').addEventListener('click', function () {
    var generateBtn = document.getElementById('generate-btn');
    // generateBtn.style.display = 'none';
    generateBtn.disabled = true;

    var prompt = document.getElementById('suggested-prompt').value;

    // add "realistic photography style," to the prompt
    prompt += ', realistic photography style';

    // Make a POST request to the backend server
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({prompt: prompt}),

        // hide "Generate" button
        // show loading spinner
        // disable the "Generate" button

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
                // Create the structure as per the format
                const frame8Div = document.createElement('div');
                frame8Div.classList.add('frame-8');

                const groupDiv = document.createElement('div');
                groupDiv.classList.add('group');
                frame8Div.appendChild(groupDiv);

                const overlapGroupDiv = document.createElement('div');
                overlapGroupDiv.classList.add('overlap-group');
                groupDiv.appendChild(overlapGroupDiv);

                const frameImageDiv = document.createElement('div');
                frameImageDiv.classList.add('frame-image');
                frameImageDiv.style.backgroundImage = `url(${imageUrl})`;
                overlapGroupDiv.appendChild(frameImageDiv);

                const component2Div = document.createElement('div');
                component2Div.classList.add('component-2');
                frame8Div.appendChild(component2Div);

                const selectButton = document.createElement('button');
                selectButton.innerText = 'Select';
                selectButton.classList.add('button');
                component2Div.appendChild(selectButton);
                selectButton.addEventListener('click', function () {

                    // Deselect any previously selected image and button
                    //document.querySelectorAll('.selected-img').forEach(img => img.classList.remove('selected-img'));
                    document.querySelectorAll('.button-2').forEach(btn => btn.classList.replace('button-2', 'button'));
                    document.querySelectorAll('.overlap-group-wrapper').forEach(div => div.classList.replace('overlap-group-wrapper', 'overlap-group'));
                    document.querySelectorAll('.vector-wrapper').forEach(div => div.remove());
                    document.querySelectorAll('.button-wrapper').forEach(div => div.classList.replace('button-wrapper', 'component-2'));

                    // Highlight the selected image and button
                    overlapGroupDiv.classList.replace('overlap-group', 'overlap-group-wrapper');
                    // right under frame image, add
                    // <div class="vector-wrapper">
                    //      <img class="vector" src="https://c.animaapp.com/YGZ9wAHJ/img/vector-10-1.svg" />
                    // </div>
                    const vectorWrapperDiv = document.createElement('div');
                    vectorWrapperDiv.classList.add('vector-wrapper');
                    overlapGroupDiv.appendChild(vectorWrapperDiv);
                    const vectorImg = document.createElement('img');
                    vectorImg.classList.add('vector');
                    vectorImg.src = 'https://c.animaapp.com/YGZ9wAHJ/img/vector-10-1.svg';
                    vectorWrapperDiv.appendChild(vectorImg);
                    // highlight the select button
                    // change button class from button to button-2
                    selectButton.classList.replace('button', 'button-2');
                    // change component-2 to button-wrapper
                    component2Div.classList.replace('component-2', 'button-wrapper');

                    // Fill the selected image into the selected-image-frame
                    // change frame-13 background image to the selected image
                    const frame13 = document.getElementById('frame-13');
                    frame13.style.backgroundImage = `url(${imageUrl})`;
                    // change picture-wrapper border invisible
                    const pictureWrapper = document.getElementById('picture-wrapper');
                    pictureWrapper.style.border = 'none';

                    // Enable the confirm button when an image is selected and user-words are entered
                    const userWords = document.getElementById('user-words');
                    if (userWords.value.trim()) {
                        document.getElementById('confirm-btn').disabled = false;
                    }
                });

                generatedImagesContainer.appendChild(frame8Div);
                generateBtn.disabled = false;
            });

            // Show confirm button after all images have been displayed
            document.getElementById('confirm-btn').style.display = 'block';

        })
        .catch(error => {
            console.error('Caught an error:', error);
        });
});

document.getElementById('confirm-btn').addEventListener('click', function () {
    var prompt = document.getElementById('suggested-prompt').value;
    var selectedImage = document.querySelector('.frame-13').style.backgroundImage;

    // Open the modal
    var modal = document.getElementById('creator-modal');
    modal.style.display = 'block';

    // Enable the submit button when the user enters their name
    document.getElementById('creator-name').addEventListener('input', function () {
        var submitBtn = document.getElementById('submit-btn');
        if (this.value) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    });

    // Save the data into the database when the form is submitted
    document.getElementById('creator-form').addEventListener('submit', function (e) {
        e.preventDefault();
        var creatorName = document.getElementById('creator-name').value;
        var themeId = document.getElementById('theme-id').value;
        var prompt = document.getElementById('suggested-prompt').value;
        var selectedImage = document.getElementById('frame-13').style.backgroundImage;
        var content = document.getElementById('user-words').value;

        // TODO - Remove the hardcoded URL
        // the selected image: url("/static/generated/samples/00605.png")
        // use expression it to "/static/generated/samples/00605.png"
        selectedImage = selectedImage.match(/url\("(.*)"\)/)[1];

        // Make a POST request to the backend server
        fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                image: selectedImage,
                creator: creatorName,
                theme_id: themeId,
                content: content
            }),
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
    // document.getElementsByClassName('close-btn')[0].onclick = function () {
    //     modal.style.display = 'none';
    // }

    // Close the modal when the user clicks outside of the modal
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});


function addPrompt(prompt) {
    var textarea = document.getElementById('suggested-prompt');
    if (textarea.value.length > 0) {
        textarea.value += ', ';
    }
    textarea.value += prompt;

    var generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = false;
}

document.getElementById('suggested-prompt').addEventListener('input', function () {
    var generateBtn = document.getElementById('generate-btn');
    if (this.value.trim()) {
        generateBtn.disabled = false;
    } else {
        generateBtn.disabled = true;
    }
});

document.querySelector('.button-3').addEventListener('click', function () {
    window.location.href = '/';
});

document.getElementById('user-words').addEventListener('input', function () {
    // if frame-13 background image is not empty and user-words is not empty, enable confirm button
    var frame13 = document.getElementById('frame-13');
    var confirmBtn = document.getElementById('confirm-btn');
    if (frame13.style.backgroundImage && this.value.trim()) {
        confirmBtn.disabled = false;
    } else {
        confirmBtn.disabled = true;
    }
});