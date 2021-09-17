const token = Cookies.get('token');
const elements ={

    questions: document.getElementById("questions"),
    headers: { 'headers': { 'Authorization': `Bearer ${token}` } }     
}
getQuestions()
function getQuestions(event) {

    axios.get(`/questions`, elements.headers)
    .then(function (response) {
        elements.questions.innerHTML = response.data.map((v) => {

            return `<li><a href="answers.html?question=${question}">${v[0]} ${v[1]} ${v[2]}</a></li>`
        
        }).join("\n")
    })
    .catch(function (error) {
        console.log(error);
    });
}

function addItem(event) {
    if (event.keyCode == 13) {
        axios.post('/question', { 'question' : newQuestion.value }, elements.headers)
            .then(function (response) {
                newQuestion.value = "";
            })
            .catch(function (error) {
                console.log(error);
            })
            .then(function () {
                // always executed
            });
        getQuestions();
    }
}
