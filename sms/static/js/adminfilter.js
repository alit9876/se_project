
document.addEventListener("DOMContentLoaded", () => {
    const filterBtn = document.getElementById("filter-btn");
    const filterDropdown = document.getElementById("filter-dropdown");
  
    // Toggle dropdown visibility when filter button is clicked
    filterBtn.addEventListener("click", (event) => {
      event.stopPropagation(); // Prevent click from closing dropdown
      filterDropdown.style.display =
        filterDropdown.style.display === "block" ? "none" : "block";
    });
  
    // Hide dropdown when clicking outside of it
    document.addEventListener("click", () => {
      filterDropdown.style.display = "none";
    });
  });
  