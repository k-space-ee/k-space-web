$(document).ready(function(){
  $('.parallax').parallax();

  const TIMEOUT = 4000;
  const LENGTH = 3;

  let n = 2;

  let loopInterval = setInterval(()=> {

    let images = $('.fadeimage');
    let image = $('.fadeimage:nth-child(' + (n) + ')');
    let next = n < LENGTH ? n++ : n=1;

    // images.css('opacity', 0)
    // image.css('opacity', 1)
    // console.log()
    // console.log(image);
    // console.log(image.css('opacity', 1))
  }, TIMEOUT);




});
