const btnAddPhotos = document.querySelector(".add_photos")
const btnSendPhotos = document.querySelector(".btn__send__photos")

const photos = document.querySelector("#Photos")
const ContainerPhotos = photos.querySelector(".container")
let PhotosForm = ContainerPhotos.querySelector("#form__photos")
let photoslistInputs = PhotosForm.querySelector(".inputs")
const site = "http://merge-video.com/" 

let modal = document.querySelector("#popup")
let closeModal = document.querySelector(".btn__close")
let modalBtns = document.querySelector(".btns__popup")
let modalText = document.querySelector(".text_popup")

let body = document.querySelector("body")

let payBtn = document.querySelector(".btn__pay")
let chekPayBtn = document.querySelector(".chek__pay")
/* Creating an input field for YouTube playlist links*/
btnAddPhotos.addEventListener('click', () =>{
    let input = document.createElement('input')
    input.classList.add('form-input')
    input.classList.add('video_input')
    input.placeholder = "Paste link"
    input.id = "formGroupExampleInput"

    photoslistInputs.appendChild(input)
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

/* Sending videos on server */
btnSendPhotos.addEventListener('click',(e) =>{
    $('.preloader').addClass('active')
    let links = []
    e.preventDefault()
    let formData = new FormData(PhotosForm)
    formData.delete("csrf_token")
    for(let [name, value] of formData){
        if(value.length != 0){
            links.push(value)
        }     
    }
    if(links.length < 2){
        PhotosForm.reset()
        $('.preloader').removeClass('active')
        alert("You can't merge less than two videos")
    }else{
        let data = JSON.stringify({"link": links})
        let response = $.ajax({
            method: 'POST',
            dataType: "json",
            url: `${site}/photos`,
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
          PhotosForm.reset()
    }
})