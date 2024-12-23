document.addEventListener('DOMContentLoaded', function () {
  const eventItems = document.querySelectorAll('.event-item');
  
  // Add the line between events only if there are two or more events
  if (eventItems.length > 1) {
    for (let i = 0; i < eventItems.length - 1; i++) {
      eventItems[i].classList.add('event-item-with-line');
    }
  }
});

function toggleDetails(button) {
  const eventItem = button.closest('.event-item');
  const eventDetails = eventItem.querySelector('.event-full-details');
  
  const isCurrentlyVisible = eventDetails.style.display === 'block';
  eventDetails.style.display = isCurrentlyVisible ? 'none' : 'block';
  
  button.textContent = isCurrentlyVisible ? 'More Info' : 'Hide Info';
}
