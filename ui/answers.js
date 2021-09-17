const token = Cookies.get('token');
const elements ={

    question: document.getElementById("question"),
    headers: { 'headers': { 'Authorization': `Bearer ${token}` } }     
}

function postAnswer(event) {

    if(event.keyCode == 13) {

        axios.post(elements.question, elements.headers)
            .then(function (response) {
                newQuestion.value = "";
            })
            .catch(function (error) {
                console.log(error);
            })
            .then(function () {
                // always executed
            });
    }
}