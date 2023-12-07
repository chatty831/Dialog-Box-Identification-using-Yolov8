function handleDropdownItemClick(option) {
    // Do something with the selected option, e.g., update a hidden input or perform an action
    document.getElementById('modelDropdown').innerText = option;

    const url = '/send_model'
    const data = { stringData: option }
    axios.post(url, data)
    // Optionally, prevent the default behavior (changing the URL)
    event.preventDefault();
}

function showChangedPreview() {
    const changedPreviewElement = document.getElementById('changedPreview');
    if (changedPreviewElement) {
        changedPreviewElement.style.display = 'block';
    }
}

function hideChangedPreview() {
    const changedPreviewElement = document.getElementById('changedPreview');
    if (changedPreviewElement) {
        changedPreviewElement.style.display = 'none';
    }
}

function GenerateImage() {
    axios.get('/generate')
        .then(function (response) {
            // console.log('Image generated successfully', response.data.result)
            if (response.data.error) {
                alert(response.data.error);
                return;
            }
            const changed_image_path = response.data.changed_image;
            console.log('The changed path', changed_image_path);
            const changed_image_element = document.getElementById("ChangedImagePreview");
            if(changed_image_path){
                changed_image_element.src = changed_image_path;
            }
            showChangedPreview();

        })

        .catch(function (error) {
            alert('Please select a model.')
        })
}

function toggleOriginalImage() {
    var originalPreview = document.getElementById("originalPreview");
    var checkbox = document.getElementById('toggleOriginalImage');

    originalPreview.style.display = checkbox.checked? 'none' : 'block';
}