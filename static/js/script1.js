// (function(){
//     "use strict";
//     new PureCounter();


    
//   /**
//    * Frequently Asked Questions Toggle
//    */
//   document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
//     faqItem.addEventListener('click', () => {
//       faqItem.parentNode.classList.toggle('faq-active');
//     });
//   });

//   console.log("Hello");
// });

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
        faqItem.addEventListener('click', () => {
            faqItem.parentNode.classList.toggle('faq-active');
        });
    });

    console.log("hello");
});
