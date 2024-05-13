// Function to handle when an image is selected
function handleImageSelect(event) {
    var selectedFile = event.target.files[0];

    if (!selectedFile) {
        return;
    }

    // Create a FileReader object to read the selected file
    var reader = new FileReader();

    // Callback function when FileReader finishes loading the file
    reader.onload = function(event) {
        var imgSrc = event.target.result;

        // Create a new image element
        var img = document.createElement('img');

        // Set the source of the image
        img.src = imgSrc;
        img.classList.add("w-50")
        // Set optional attributes
        img.alt = 'Preview Image';

        // Clear previous image (if any)
        var imageContainer = document.getElementById('image-container');
        imageContainer.innerHTML = '';

        // Append the image to the container
        imageContainer.appendChild(img);
    };

    // Read the selected file as a data URL
    reader.readAsDataURL(selectedFile);
}

// Add event listener to the file input element
document.getElementById('image-input').addEventListener('change', handleImageSelect);
