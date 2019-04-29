function show_selected(name) {
    check_boxes = document.getElementsByName(name)
    for (var i=0;i<check_boxes.length;i++){
        if ( check_boxes[i].checked ) {
            check_boxes[i].labels[0].setAttribute("style", "border: 3px solid #0073e6;");
        } else {
            check_boxes[i].labels[0].setAttribute("style", "border: 1px solid grey;");
        }
    }
}

function getCookie(c_name){
    console.log("document.cookie je:" + document.cookie);
    return document.cookie
}

function setCookie(c_name, value){
    document.cookie=c_name + "=" + escape(value);
}

function check() {
    unique_id = getCookie("id")
    console.log('nacitane unique id ')
    console.log(unique_id)
    if( unique_id == "" || unique_id == null){
        unique_id = new Date().getUTCMilliseconds();
        setCookie("id", unique_id);
    }
}

// Open the Modal
function openModal() {
  document.getElementById('imageModal').style.display = "block";
}

// Close the Modal
function closeModal() {
  document.getElementById('imageModal').style.display = "none";
}

window.onkeyup = function (event) {
    if (event.keyCode == 27) {
        closeModal()
    }
}

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
