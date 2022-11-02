const btnAddDrive = document.querySelector(".add_drive")
const btnSendDrive = document.querySelector(".btn__send__drive")

const drive = document.querySelector("#Drive")
const ContainerDrive = drive.querySelector(".container")
let drivetForm = ContainerDrive.querySelector("#form__drive")
let drivelistInputs = drivetForm.querySelector(".inputs")

let modal = document.querySelector("#popup")
let closeModal = document.querySelector(".btn__close")
let modalBtns = document.querySelector(".btns__popup")
let modalText = document.querySelector(".text_popup")

let body = document.querySelector("body")

let payBtn = document.querySelector(".btn__pay")
let chekPayBtn = document.querySelector(".chek__pay")

const site = "http://merge-video.com" 


/* Creating an input field for YouTube playlist links*/
btnAddDrive.addEventListener('click', () =>{
    let input = document.createElement('input')
    input.classList.add('form-input')
    input.classList.add('video_input')
    input.placeholder = "Paste link"
    input.id = "formGroupExampleInput"

    drivelistInputs.appendChild(input)
})

$(document).ready(function() {
    $('.preloader').fadeOut(400);
});


function btnCancel(){
    let btn = document.createElement('button')
    btn.classList = "btn btn__main btn__close"
    btn.innerHTML = "Cancel"
    return btn
}

function formEmail(){
    let formEmail = document.createElement('div')
    formEmail.classList = "from-email input-group mb-3"
    let input = document.createElement('input')
    input.type = "email"
    input.classList = "form-input email_input"
    input.placeholder = "Recipient's email"
    input.setAttribute = ("aria-label","Recipient's username")
    input.setAttribute = ("aria-describedby","button-addon2")
    let btn = document.createElement('button')
    btn.classList = "btn btn-outline-secondary send_mail"
    btn.type = "button"
    btn.id = "button-addon2"
    btn.innerHTML = "Send"
    formEmail.appendChild(input, btn)
    formEmail.appendChild(btn)
    return formEmail
}

function validateEmail(email) {
    var re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    return re.test(String(email).toLowerCase());
}

/* Sending playlist on server */
btnSendDrive.addEventListener('click',(e) =>{
    $('.preloader').addClass('active')
    let links = []
    e.preventDefault()
    let formData = new FormData(drivetForm)
    formData.delete("csrf_token")
    for(let [name, value] of formData){
        if(value.length != 0){
            links.push(value)
        }     
    }
    if(links.length < 2){
        drivetForm.reset()
        $('.preloader').removeClass('active')
        alert("You can't merge less than two videos")
    }else{
        let data = JSON.stringify({"link": links})
        let response = $.ajax({
            method: 'POST',
            dataType: "json",
            url: `${site}/drive_links`,
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
                    modalText.innerHTML = `You want to mount ${links.length} videos<br>
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
          drivetForm.reset()
    }
})