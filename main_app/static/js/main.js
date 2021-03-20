// const nav = document.getElementById('nav');
//   window.onscroll = function(){
//     if (window.pageXOffset >100) {
//       nav.style.background = "black";
//     } 
//     else {
//       nav.style.background = "transparent"
//     }
//   }

const slider = document.querySelector(".slider");
    M.Slider.init(slider, {
      indicators: false,
      height: 600,
      transition: 500,
      interval: 5000
    })



  