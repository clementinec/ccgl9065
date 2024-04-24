let data; // Declare the variable to hold your JSON data

fetch('student.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(jsonData => {
        data = jsonData; // Assign the fetched data to the global 'data' variable
        console.log(data); // Log the data to ensure it's loaded
        // Initialize the content with the default UID after data is loaded
        updateContent('UID1');
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

function displayData(uid) {
    const userData = data[uid];
    const container = document.getElementById('content'); // Correct ID
    if (!userData) {
        container.innerHTML = `<h2>No data available for ${uid}</h2>`;
        return;
    }
    container.innerHTML = `
        <h2>Data for ${uid}</h2>
        <p>${userData.text}</p>
        <img src="${userData.image}" alt="Image for ${uid}" style="width: 100%; max-width: 600px;">
        <iframe src="${userData.video}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width: 100%; height: 300px;"></iframe>
    `;
}


function updateContent(uid) {
  console.log("Called updateContent with UID:", uid);
  // If no UID is provided, use a default one
  uid = uid || "UID1"; // Default UID
  console.log("Using UID:", uid);

  // Check if the UID exists in the data object
  if (data && data[uid]) { // Also checking if data is loaded
    console.log("Updating content for UID:", uid);
    // Update image content
    document.getElementById("dynamicImage").src = data[uid]["image"];
    // Update video content
    document.getElementById("dynamicVideo").src = data[uid]["video"];
    // Update text content
    document.getElementById("dynamicText").textContent = data[uid]["text"];
  } else {
    // Handle case where UID is not found in the data object
    console.error("UID not found or data not loaded:", uid);
    alert("UID not found. Please check the input and try again.");
  }
}

// Add event listener to the button to update content based on input
document.getElementById("updateContent").addEventListener("click", function() {
  var uid = document.getElementById("uidInput").value;
  updateContent(uid);
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("updateContent").addEventListener("click", function() {
      var uid = document.getElementById("uidInput").value;
      updateContent(uid);
    });

    document.getElementById("uidInput").addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
        event.preventDefault(); // Prevent the default action to stop form submission
        var uid = document.getElementById("uidInput").value;
        updateContent(uid);
      }
    });
});
