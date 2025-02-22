
// Initialize animations on page load
document.addEventListener('DOMContentLoaded', () => {
  const elements = document.querySelectorAll('.fade-in, .slide-in');
  elements.forEach(element => {
    // Add the animation class to trigger the effect
    element.classList.add('animate');
  });
});
document.addEventListener('DOMContentLoaded', () => {
  const heading = document.querySelector('.animated-heading');
  heading.classList.add('animate');
});

 const timelineItems = document.querySelectorAll('.timeline-item');

    function showVisibleItems() {
      const triggerHeight = window.innerHeight / 1.2;

      timelineItems.forEach(item => {
        const itemTop = item.getBoundingClientRect().top;

        if (itemTop < triggerHeight) {
          item.classList.add('visible');
        }
      });
    }

    // Event listener for scrolling
    window.addEventListener('scroll', showVisibleItems);

    // Trigger on page load
    showVisibleItems();


