function checkSolution() {
    const inputs = document.querySelectorAll('.sudoku-cell input');
    const solution = {{ solved_puzzle | tojson }};
    let correct = true;

    // Reset previous errors
    inputs.forEach(input => {
        input.style.backgroundColor = '';  // Clear previous red highlights
        input.disabled = false;  // Enable inputs for re-checking
    });

    // Check if user input matches solution
    inputs.forEach((input, index) => {
        const row = Math.floor(index / 9);
        const col = index % 9;
        const correctValue = solution[row][col];

        if (input.value && parseInt(input.value) !== correctValue) {
            input.style.backgroundColor = 'red';  // Highlight incorrect cells
            correct = false;
            input.disabled = true;  // Disable input if it is wrong
        }
    });

    // Show message if the solution is correct or not
    if (correct) {
        alert("Congratulations! All values are correct.");
    } else {
        alert("There are some incorrect values!");
    }
}
