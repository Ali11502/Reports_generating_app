console.log("hellow world")
const reportBtn=document.getElementById('report_btn')
const img=document.getElementById('img')
const modalBody=document.getElementById('modal-body')
const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const reportForm = document.getElementById('report-form')
const alertBox = document.getElementById('alert-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const handleAlerts = (type, msg) =>{
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}
if(img){
    reportBtn.classList.remove('not-visible')
}
reportBtn.addEventListener('click',()=>
    {console.log('clicked')
        img.setAttribute('class','w-100')
        modalBody.prepend(img)
        reportForm.addEventListener('submit',e=>{
        //    we don't want to refresh page but we want to keep doing work so that is why 
        // we prevent default
            e.preventDefault()
            const formData=new FormData()
            // we will be sending the below data through ajax request to report model
            formData.append('csrfmiddlewaretoken',csrf)
            formData.append('name',reportName.value)
            formData.append('remarks', reportRemarks.value)
            formData.append('image', img.src)

            $.ajax({
                type:'POST',
                // url of logic that will save report object
                url:'/reports/save/',
                data: formData,
                success:function(response){
                    console.log(response)
                    handleAlerts('success', 'report created')
                },
                error:function(error){
                    console.log(error)
                    handleAlerts('danger', 'something went wrong')

                },
                processData:false,
                contentType:false,
            })
        })


    }
)