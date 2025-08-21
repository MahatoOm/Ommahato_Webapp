// // Simple scroll animation (optional)
// document.addEventListener("DOMContentLoaded", () => {
//     const sections = document.querySelectorAll("section");
//     sections.forEach(section => {
//       section.style.opacity = 0;
//       section.style.transition = "opacity 0.6s ease-in-out";
//       const observer = new IntersectionObserver(([entry]) => {
//         if (entry.isIntersecting) {
//           section.style.opacity = 1;
//         }
//       });
//       observer.observe(section);
//     });
//   });



// from project 2
var tablinks = document.getElementsByClassName("tab-links")
var tabcontents = document.getElementsByClassName("tab-contents")
function opentab(tabname){
    for(tablink of tablinks){
        tablink.classList.remove("active-link");
    }
    for(tabcontent of tabcontents){
        tabcontent.classList.remove("active-tab");
    }
    event.currentTarget.classList.add("active-link");
    document.getElementById(tabname).classList.add("active-tab")
}

let currentIndex = 0;
let score = 0;
let test = false;

function showQuestion(index) {
    let q = window.questions[index];
    document.getElementById("question").innerText = window.questions[index].question;
    document.getElementById("option1").innerText = window.questions[index].option1;
    document.getElementById("option2").innerText = window.questions[index].option2;
    document.getElementById("option3").innerText = window.questions[index].option3;



// clear previous responses
let radios = document.getElementsByName("option");
radios.forEach(r => r.checked = false);
}

function submit(){
    let selected = document.querySelector('input[name="option"]:checked');
    if (!selected){
        alert("Please select an answer before moving on!");
        return;
    }
    let flashMessage = document.getElementById("flash-message");

    let answer = selected.value; // option1 option2 option3
    
    let correctAnswer = window.questions[currentIndex].ans.toLowerCase();

    if (window.questions[currentIndex][answer].toLowerCase() == correctAnswer){
        test = true;
        flashMessage.textContent = "✅ Correct! Your Score: " + (score+1) ;
        flashMessage.style.color = "green";
        test = true;
        
    } else{
        
        flashMessage.textContent = "❌ Wrong! Your Score: " +( score) ;
        flashMessage.style.color = "red" 
        test= false;
    }       

}

function nextQuestion() {
    let selected = document.querySelector('input[name="option"]:checked');
    if (!selected) {
        alert("Please select an answer before moving on!");
        return;
    }

    let answer = selected.value; // option1 option2 option3
    let correctAnswer = window.questions[currentIndex].ans.toLowerCase();

    if ((window.questions[currentIndex][answer].toLowerCase() == correctAnswer) || (test == true)) {
        score++;
    }

    // move to next question
    currentIndex++;

    // clear flash
    let flashMessage = document.getElementById("flash-message");
    flashMessage.textContent = "";

    // check if quiz is finished
    if (currentIndex >= window.questions.length) {
        document.querySelector(".mcq_head").innerHTML = `
          <h2>🎉 Quiz Finished! 🎉</h2>
          <p>You scored ${score} out of ${window.questions.length}</p>
        `;
        return;
    }

    showQuestion(currentIndex);
}


// Show the first question when the page loads
document.addEventListener("DOMContentLoaded", () => {
    showQuestion(currentIndex);
});


  