


document.addEventListener('DOMContentLoaded', function() { // связь с DOM
  const sliders = document.querySelectorAll('.slider'); // выбираем все слайдеры
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  

  sliders.forEach(slider => { // для каждого слайдера 
      let currentIndex = 0; // текущий слайд по индексу
      const slides = slider.querySelectorAll('.slide'); // выбираем все слайды

      function showSlide(index) { // показать слайд по индексу
          slides.forEach((slide, i) => { 
              slide.style.display = i === index ? 'block' : 'none'; // показать слайд по индексу 
          });
      }

       prevBtn.addEventListener('click', function() { // предыдущий слайд по индексу
        currentIndex = (currentIndex - 1 + slides.length) % slides.length; // индекс предыдущего слайда
        showSlide(currentIndex); // показать предыдущий слайд
      });

      nextBtn.addEventListener('click', function() { // следующий слайд по индексу
        currentIndex = (currentIndex + 1) % slides.length; // индекс следующего слайда
        showSlide(currentIndex); // показать следующий слайд

      });

      

    //   function nextSlide() { // следующий слайд по индексу 
    //       currentIndex = (currentIndex + 1) % slides.length; // индекс следующего слайда
    //       showSlide(currentIndex); // показать следующий слайд


    //   }

    //   setInterval(nextSlide, 3000); // следующий слайд каждые 3 секунды
      showSlide(currentIndex);
      
  });

  
});