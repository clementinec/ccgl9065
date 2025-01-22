let data; // Declare the variable to hold your JSON data

// Fetch the JSON data
fetch('student.json')
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then((jsonData) => {
    data = jsonData; // Assign the fetched data to the global 'data' variable
    console.log('Data loaded:', data);
  })
  .catch((error) => {
    console.error('Error fetching or processing student.json:', error);
  });

// Randomize and display a portfolio
function randomizeContent() {
  if (data) {
    const students = Object.keys(data); // Get all student UIDs
    const randomUID = students[Math.floor(Math.random() * students.length)]; // Pick a random UID
    updateContent(randomUID); // Use the existing updateContent function
  } else {
    console.error('Data not loaded. Cannot randomize content.');
    alert('Data not loaded. Please try again later.');
  }
}

// Existing updateContent function
function updateContent(uid) {
  if (data && data[uid]) {
    document.getElementById('dynamicImage').src = data[uid].image || 'placeholder.jpg';
    document.getElementById('dynamicVideo').src = data[uid].video || '';
    document.getElementById('dynamicText').textContent = data[uid].text || 'No information available.';
  } else {
    console.error('UID not found:', uid);
    alert('The selected student portfolio could not be found.');
  }
}

// Event listener for randomization button
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('randomizeContent').addEventListener('click', randomizeContent);
});
