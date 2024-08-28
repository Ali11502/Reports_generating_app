// Fetch the CSRF token from the HTML document
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

// Get the alert box element from the HTML document
const alertBox = document.getElementById('alert-box')

// Disable automatic discovery of Dropzone elements
Dropzone.autoDiscover = false

// Function to handle alert messages
const handleAlerts = (type, msn) =>{
    // Set the inner HTML of the alert box to display the alert message
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msn}
    </div>
    `
}

// Initialize a new Dropzone instance with specific configuration
const myDropzone = new Dropzone('#my-dropzone', {
    // The URL to which files will be uploaded (commented out)
    // url: '/reports/upload/',
    url:'/reports/upload/',  // The actual URL to which files will be uploaded
    init: function(){
        // Event listener for when a file is being sent
        this.on('sending', (file, xhr, formData)=>{
            console.log('sending')
            // Append the CSRF token to the form data
            formData.append('csrfmiddlewaretoken', csrf)
        })
        // Event listener for when a file upload is successful
        this.on('success', function(file, response){
            console.log(response)
            const ex = response.ex
            // If the response indicates the file already exists, show an error alert
            if (ex){
                handleAlerts('danger', 'File already exists.')
             }else{
                // Otherwise, show a success alert
                handleAlerts('success', 'Your file has been uploaded.')
            }
        })
    },
    // Maximum number of files that can be uploaded
    maxFiles: 3,
    // Maximum file size in MB
    maxFilesize: 3,
    // Accepted file types
    acceptedFiles: '.csv'
})
