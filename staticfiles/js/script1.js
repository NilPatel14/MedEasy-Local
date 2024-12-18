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
    
        // Animation for hero section
      const heroSection = document.getElementById("hero");
      
      if (heroSection) {
          console.log("herosection");
        setTimeout(() => {
          console.log("Class added");
          heroSection.classList.add("show");
        }, 500);
      } else {
        console.error("Element with ID 'hero' not found in the DOM.");
      }
      
    

    // Animation for about 
    const aboutSection = document.querySelector(".about");

  window.addEventListener("scroll", () => {
    if (heroSection && aboutSection) {
      const heroBottom = heroSection.getBoundingClientRect().bottom;

      // Trigger animation when the bottom of hero section is scrolled
      if (heroBottom < window.innerHeight / 1.2) {
        aboutSection.classList.add("show");
      } else {
        aboutSection.classList.remove("show");
      }
    }
  });


        // Animation for services
        const serviceItems = document.querySelectorAll('.service-item');

  function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom >= 0;
  }

  window.addEventListener('scroll', function () {
    if (isElementInViewport(aboutSection)) {
      serviceItems.forEach((item, index) => {
        if (!item.classList.contains('visible')) {
          setTimeout(() => {
            if (index % 2 === 0) {
              item.classList.add('show-left');
            } else {
              item.classList.add('show-right');
            }
            item.classList.add('visible');
          }, index * 300);
        }
      });
    }
  });

    //Animation for contact
    const contactSection = document.querySelector(".contact");
    const gallarySection = document.querySelector(".gallery");

    window.addEventListener("scroll", () => {
      if (gallarySection && contactSection) {
        const gallaryBottom = gallarySection.getBoundingClientRect().bottom;
  
        // Trigger animation when the bottom of hero section is scrolled
        if (gallaryBottom < window.innerHeight / 1.2) {
            contactSection.classList.add("show");
        } else {
            contactSection.classList.remove("show");
        }
      }
    });


    document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
        faqItem.addEventListener('click', () => {
            faqItem.parentNode.classList.toggle('faq-active');
        });
    });

    console.log("hello");

});

