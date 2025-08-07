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


  