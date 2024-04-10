document.querySelectorAll('.container').forEach(function(container, index) {
  container.addEventListener('click', function() {
    // First, remove 'selected' class from all containers
    document.querySelectorAll('.container.selected').forEach(function(selectedContainer) {
      selectedContainer.classList.remove('selected');
    });

    // First, hide all .component-wrapper elements
    document.querySelectorAll('.component-wrapper').forEach(function(wrapper) {
      wrapper.style.display = 'none';
    });

    // Then, add 'selected' class to the clicked container
    container.classList.add('selected');

    // Then, show the .component-wrapper corresponding to the clicked .container
    document.querySelectorAll('.component-wrapper')[index].style.display = 'flex';

  });
});


function reportFake(fakeIndex, userChoice, questionId) {
    if (userChoice == 1) {
        console.log("Correct: User thinks the question is fake");
    }
    else {
        console.log("Incorrect: User thinks the question is real");
    }
    // for the questionId Container, we need to show the mask of the question, and show "frame-9" in side

    const selectedContainer = document.querySelectorAll('.container')[fakeIndex];
    // Create a new div element for the mask
    const mask = document.createElement('div');
    mask.style.position = 'absolute';
    mask.style.top = '0';
    mask.style.left = '0';
    mask.style.width = '100%';
    mask.style.height = '100%';
    mask.style.borderRadius = '10px';
    mask.style.background = 'rgba(0, 0, 0, 0.5)'; // Change this to the color and transparency you want
    // Append the mask to the selected container
    selectedContainer.appendChild(mask);

    // Get the "frame-9" element and set its display to flex
    const frame9 = selectedContainer.querySelector('.frame-9');
    frame9.style.display = 'flex';


    //Send the user's choice to the server, and save it in the database

    fetch('/report_fake', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_choice: userChoice, question_id: questionId })
    })
    .then(response => response.json())
    .then(data => {
        // 'is_correct': is_correct, 'percentage_correct': percentage_correct, 'n_answers': n_answers, 'n_correct': n_correct
        const isCorrect = data.is_correct;
        const totalAnswers = data.n_answers;
        const correctAnswers = data.n_correct;
        var percentageCorrect = Math.round(data.percentage_correct);
        // round to integer
        percentageCorrect = Math.round(percentageCorrect);


        updatePage(isCorrect, totalAnswers, correctAnswers, percentageCorrect);
    })
    .catch(error => console.error('Error:', error));
}

function updatePage(isCorrect, totalAnswers, correctAnswers, percentageCorrect) {
    console.log("Updating page");

    // Make class=Tweet flex
    document.querySelector('.tweet').style.display = 'flex';

    // According to the user's choice, update foolTitle and foolMessage or CorrectTitle and CorrectMessage, hide the unselected one
    if (isCorrect) {
        document.getElementById('foolTitle').style.display = 'none';
        document.getElementById('foolMessage').style.display = 'none';
        document.getElementById('correctTitle').style.display = 'block';
        document.getElementById('correctMessage').style.display = 'block';
    }
    else {
        document.getElementById('foolTitle').style.display = 'block';
        document.getElementById('foolMessage').style.display = 'block';
        document.getElementById('correctTitle').style.display = 'none';
        document.getElementById('correctMessage').style.display = 'none';
    }

    // Update the percentage of correct answers - text-wrapper-10
    document.getElementById('percentageCorrect').innerHTML = (100-percentageCorrect) + "%";

    // Update the number of correct answers - text-wrapper-12
    document.getElementById('correctAnswers').innerHTML = correctAnswers;

    // Update the total number of answers - text-wrapper-12
    document.getElementById('totalAnswers').innerHTML = totalAnswers;

    // Update the progress bar
    let progress = document.getElementById('progress');
    let grayCat = document.querySelector('.gray-cat');
    let percentage = 100-percentageCorrect; // This should be your actual percentage

    // Adjust the width of the progress bar
    progress.style.width = percentage + '%';

    // Adjust the position of the gray-cat
    grayCat.style.left = percentage + '%';


    // all the containers couldn't be clicked anymore
    document.querySelectorAll('.container').forEach(function(container) {
        container.style.pointerEvents = 'none';
    });
    // Disable all the buttons
    document.querySelectorAll('.button').forEach(function(button) {
        button.style.pointerEvents = 'none';
    });

}