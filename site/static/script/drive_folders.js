const btnAddFolders = document.querySelector(".add_folders")
const btnSendFolders = document.querySelector(".btn__send__folders")

const folder = document.querySelector("#Drive-folder")
const ContainerFolder = folder.querySelector(".container")
let foldersForm = ContainerFolder.querySelector("#form__folders")
let folderslistInputs = foldersForm.querySelector(".inputs")


/* Creating an input field for YouTube playlist links*/
btnAddFolders.addEventListener('click', () =>{
    let input = document.createElement('input')
    input.classList.add('form-input')
    input.classList.add('video_input')
    input.placeholder = "Paste link"
    input.id = "formGroupExampleInput"

    folderslistInputs.appendChild(input)
})

/* Sending videos on server */
btnSendFolders.addEventListener('click',(e) =>{
    $('.preloader').addClass('active')
    let links = []
    e.preventDefault()
    let formData = new FormData(foldersForm)
    formData.delete("csrf_token")
    for(let [name, value] of formData){
        if(value.length != 0){
            links.push(value)
        }     
    }
    let data = JSON.stringify({"link": links})
    let response = $.ajax({
        method: 'POST',
        dataType: "json",
        url: `${site}/drive_folders`,
        data: data,
        headers:{ "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"},
        success: function(data) {
            $('.preloader').removeClass('active')
            if(data == "0"){
                alert("You sent incorrect links, please try again")
            }
            else if(Number(data["videos"]["size"]) < 10){
                alert("Price is small")
                let response = $.ajax({
                    method: 'POST',
                    dataType: "json",
                    url: `${site}/delete`,
                    data: JSON.stringify({"videos":data["videos"]["videos"]}),
                    headers:{ "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*"} 
                })
            }
            else{
                $('.btns__popup').addClass('active')
                modal.style.display = "block"
                body.style.overflow = "hidden"
                payBtn.href = data["pay_url"]
                modalText.innerHTML = `You want to mount ${data["videos"]["videos"].length} videos<br>
                Video cost: ${data["videos"]["size"]} rub<br>`
                closeModal.addEventListener('click',() =>{
                    modal.style.display = "none"
                    body.style.overflow = "auto"
                    let response = $.ajax({
                        method: 'POST',
                        dataType: "json",
                        url: `${site}/delete`,
                        data: JSON.stringify({"videos":data["videos"]["videos"]}),
                        headers:{ "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"}
                    })
                })
                chekPayBtn.addEventListener('click', () =>{
                    $('.preloader').addClass('active')
                    let nameVideos = data["videos"]["videos"]
                    let name = data["comment"]
                    let req = $.ajax({
                        method: 'POST',
                        dataType: "json",
                        data: JSON.stringify({"bill_id":data["bill_id"]}),
                        url: `${site}/chek`,
                        headers:{ "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"},
                        success: function(data) {
                            $('.preloader').removeClass('active')
                            if(data == "1"){
                                modalText.innerHTML = "Video Paid! <br>Enter the email to send the finished video to:"
                                modalText.appendChild(formEmail())
                                $('.btns__popup').removeClass('active')
                                let sendMail = document.querySelector('.send_mail')

                                sendMail.addEventListener('click', () => {
                                    let email = document.querySelector('.email_input').value
                                    if(validateEmail(email)){
                                        console.log(nameVideos)
                                        let req = $.ajax({
                                            method: 'POST',
                                            dataType: "json",
                                            data: JSON.stringify({"email": email, "videos":nameVideos, "name": name}),
                                            url: `${site}/merge`,
                                            headers:{ "Content-Type": "application/json",
                                            "Access-Control-Allow-Origin": "*"},
                                })
                                        modalText.innerHTML = "All is ready! <br>As soon as the video is edited, it will be sent to your email automatically."
                                        let cancel = btnCancel()
                                        modalText.appendChild(cancel)
                                        cancel.addEventListener('click',() =>{
                                            modal.style.display = "none"
                                            body.style.overflow = "auto"
                                        
                                        })
                                    }else{
                                        alert("Invalid mail!")
                                    }
                                })
                            }else{
                                let t = modalText.innerHTML                 
                                if (t.includes("Not paid!") == false){
                                    modalText.innerHTML = `${t}<p style="color: red">Not paid!</p>`
                                }
                            }
                    }})
                })
            }
    }})
    foldersForm.reset()
    
})