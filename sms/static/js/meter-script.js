document.addEventListener("DOMContentLoaded", () => {
  // Hardcoded values for students and teachers
  const studentCount = 7520;  // Student count
  const totalStudentCapacity = 10000;  // Total student capacity for percentage calculation

  const teacherCount = 300;  // Teacher count
  const totalTeacherCapacity = 500;  // Total teacher capacity for percentage calculation

  // Calculate percentages
  const studentPercentage = Math.min((studentCount / totalStudentCapacity) * 100, 100);
  const teacherPercentage = Math.min((teacherCount / totalTeacherCapacity) * 100, 100);

  function animateNumber(element, targetNumber, duration) {
    let startNumber = 0;
    const increment = targetNumber / (duration / 10);
    const interval = setInterval(() => {
      startNumber += increment;
      if (startNumber >= targetNumber) {
        startNumber = targetNumber;
        clearInterval(interval);
      }
      element.textContent = Math.floor(startNumber);
    }, 10);
  }

  function animateMeter(meter, targetPercentage, duration) {
    let currentPercentage = 0;
    const increment = targetPercentage / (duration / 10);

    const colorTransition = (percentage) => {
      const r = Math.floor(255 - (percentage * 2.55));
      const g = Math.floor(percentage * 2.55);
      return `rgb(${r}, ${g}, 0)`;  // Color goes from red to green
    };

    const interval = setInterval(() => {
      currentPercentage += increment;
      if (currentPercentage >= targetPercentage) {
        currentPercentage = targetPercentage;
        clearInterval(interval);
      }
      meter.style.setProperty("--percentage", currentPercentage);
      meter.style.setProperty("--color", colorTransition(currentPercentage));
    }, 10);
  }

  function initializeMeters() {
    // Animate the student meter
    const studentMeter = document.querySelector(".meter-circle.student");
    animateMeter(studentMeter, studentPercentage, 2000);
    const studentCountElement = document.getElementById("student-count");
    animateNumber(studentCountElement, studentCount, 2000);

    // Animate the teacher meter
    const teacherMeter = document.querySelector(".meter-circle.teacher");
    animateMeter(teacherMeter, teacherPercentage, 2000);
    const teacherCountElement = document.getElementById("teacher-count");
    animateNumber(teacherCountElement, teacherCount, 2000);
  }

  // Initialize the meters
  initializeMeters();
});
