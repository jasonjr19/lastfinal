document.addEventListener('DOMContentLoaded', function() {
  
    const itineraryForm = document.getElementById('itinerary-form');
    const contactForm = document.getElementById('contact-form');

    itineraryForm.addEventListener('submit', function(event) {
      event.preventDefault();
     
      console.log('Itinerary form submitted');
    });

    contactForm.addEventListener('submit', function(event) {
      event.preventDefault();
      
      console.log('Contact form submitted');
    });
  });