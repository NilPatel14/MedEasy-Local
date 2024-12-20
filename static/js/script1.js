// // (function(){
// //     "use strict";
// //     new PureCounter();


    
// //   /**
// //    * Frequently Asked Questions Toggle
// //    */
// //   document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
// //     faqItem.addEventListener('click', () => {
// //       faqItem.parentNode.classList.toggle('faq-active');
// //     });
// //   });

// //   console.log("Hello");
// // });

// document.addEventListener('DOMContentLoaded', () => {
    
//         // Animation for hero section
//       const heroSection = document.getElementById("hero");
      
//       if (heroSection) {
//           console.log("herosection");
//         setTimeout(() => {
//           console.log("Class added");
//           heroSection.classList.add("show");
//         }, 500);
//       } else {
//         console.error("Element with ID 'hero' not found in the DOM.");
//       }
      
    

//     // Animation for about 
//     const aboutSection = document.querySelector(".about");

//   window.addEventListener("scroll", () => {
//     if (heroSection && aboutSection) {
//       const heroBottom = heroSection.getBoundingClientRect().bottom;

//       // Trigger animation when the bottom of hero section is scrolled
//       if (heroBottom < window.innerHeight / 1.2) {
//         aboutSection.classList.add("show");
//       } else {
//         aboutSection.classList.remove("show");
//       }
//     }
//   });


//         // Animation for services
//         const serviceItems = document.querySelectorAll('.service-item');

//   function isElementInViewport(el) {
//     const rect = el.getBoundingClientRect();
//     return rect.top < window.innerHeight && rect.bottom >= 0;
//   }

//   window.addEventListener('scroll', function () {
//     if (isElementInViewport(aboutSection)) {
//       serviceItems.forEach((item, index) => {
//         if (!item.classList.contains('visible')) {
//           setTimeout(() => {
//             if (index % 2 === 0) {
//               item.classList.add('show-left');
//             } else {
//               item.classList.add('show-right');
//             }
//             item.classList.add('visible');
//           }, index * 300);
//         }
//       });
//     }
//   });

//     //Animation for contact
//     const contactSection = document.querySelector(".contact");
//     const gallarySection = document.querySelector(".gallery");

//     window.addEventListener("scroll", () => {
//       if (gallarySection && contactSection) {
//         const gallaryBottom = gallarySection.getBoundingClientRect().bottom;
  
//         // Trigger animation when the bottom of hero section is scrolled
//         if (gallaryBottom < window.innerHeight / 1.2) {
//             contactSection.classList.add("show");
//         } else {
//             contactSection.classList.remove("show");
//         }
//       }
//     });


//     document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
//         faqItem.addEventListener('click', () => {
//             faqItem.parentNode.classList.toggle('faq-active');
//         });
//     });

//     console.log("hello");

// });

document.addEventListener('DOMContentLoaded', () => {
  // Utility: Debounce function to limit scroll event calls
  function debounce(func, wait = 20) {
      let timeout;
      return (...args) => {
          clearTimeout(timeout);
          timeout = setTimeout(() => func.apply(this, args), wait);
      };
  }

  // Utility: Check if an element is in the viewport
  function isElementInViewport(el) {
      if (!el) return false; // Avoid errors on null elements
      const rect = el.getBoundingClientRect();
      return rect.top < window.innerHeight && rect.bottom >= 0;
  }

  // Hero Section Animation
  const heroSection = document.getElementById("hero");
  if (heroSection) {
      console.log("Hero section found.");
      setTimeout(() => {
          heroSection.classList.add("show");
      }, 500);
  } else {
      console.error("Hero section not found in the DOM.");
  }

  // About Section Animation
  const aboutSection = document.querySelector(".about");
  const handleAboutSectionAnimation = () => {
      if (heroSection && aboutSection) {
          const heroBottom = heroSection.getBoundingClientRect().bottom;
          if (heroBottom < window.innerHeight / 1.2) {
              aboutSection.classList.add("show");
          } else {
              aboutSection.classList.remove("show");
          }
      }
  };

  // Service Section Animation
  const serviceItems = document.querySelectorAll(".service-item");
  const handleServiceItemsAnimation = () => {
      if (isElementInViewport(aboutSection)) {
          serviceItems.forEach((item, index) => {
              if (!item.classList.contains("visible")) {
                  setTimeout(() => {
                      const directionClass = index % 2 === 0 ? "show-left" : "show-right";
                      item.classList.add(directionClass, "visible");
                  }, index * 300);
              }
          });
      }
  };

  // Contact Section Animation
  const gallarySection = document.querySelector(".gallery");
  const contactSection = document.querySelector(".contact");
  const handleContactSectionAnimation = () => {
      if (gallarySection && contactSection) {
          const gallaryBottom = gallarySection.getBoundingClientRect().bottom;
          if (gallaryBottom < window.innerHeight / 1.2) {
              contactSection.classList.add("show");
          } else {
              contactSection.classList.remove("show");
          }
      }
  };

  // FAQ Section Toggle
  const faqItems = document.querySelectorAll(".faq-item h3, .faq-item .faq-toggle");
  faqItems.forEach((faqItem) => {
      faqItem.addEventListener("click", () => {
          faqItem.parentNode.classList.toggle("faq-active");
      });
  });

  console.log("Event listeners initialized.");

  // Attach debounced scroll events
  window.addEventListener(
      "scroll",
      debounce(() => {
          handleAboutSectionAnimation();
          handleServiceItemsAnimation();
          handleContactSectionAnimation();
      })
  );
});

// function setEmailInSession(event) {
//   event.preventDefault(); // Prevent page refresh
  
// }

// document.getElementById('sendOtpButton').addEventListener('click', function(event) {
//     console.log("OTP button clicked");
    
//     event.preventDefault(); // Prevent the form from submitting immediately

//     // Get email value
//     let email = document.getElementsByName('email')[0].value; // Access the first email field

//     // Set the cookie with the email
//     document.cookie = "email=" + encodeURIComponent(email) + "; path=/"; // You can set the expiry if needed

//     // You can add further logic here, like calling an AJAX function to send the OTP to the server

//     // Now, manually submit the form after the OTP is sent or after completing the logic
//     document.querySelector('form').submit();
// });


document.getElementById('sendOtpButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    let email = document.getElementsByName('email')[0].value; // Get email value from the form

    // Make an AJAX request to Django to send the OTP
    fetch('/send-otp/', { // Use the correct URL for your Django view
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // If you're using JSON
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // CSRF token
        },
        body: JSON.stringify({ email: email }) // Send the email in JSON body
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('OTP sent successfully!');
            alert(data.message); // Optional: Show success message to the user
        } else {
            console.log('Error:', data.message);
            alert(data.message); // Optional: Show error message
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
