document.querySelector('.submit-btn').addEventListener('click', () => {
    const rows = document.querySelectorAll('.grading-table tbody tr');
  
    rows.forEach((row) => {
      const totalMarks = parseFloat(row.querySelector('.total-marks').value);
      const obtainedMarks = parseFloat(row.querySelector('.obtained-marks').value);
      const gradeElement = row.querySelector('.grade');
  
      if (!isNaN(totalMarks) && !isNaN(obtainedMarks)) {
        const percentage = (obtainedMarks / totalMarks) * 100;
  
        let grade = '';
        if (percentage >= 90) grade = 'A+';
        else if (percentage >= 80) grade = 'A';
        else if (percentage >= 70) grade = 'B';
        else if (percentage >= 60) grade = 'C';
        else if (percentage >= 50) grade = 'D';
        else grade = 'F';
  
        gradeElement.textContent = grade;
      } else {
        gradeElement.textContent = '-';
      }
    });
  });
  