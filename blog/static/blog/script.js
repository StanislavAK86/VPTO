
document.addEventListener('DOMContentLoaded', function() { // связь с DOM
  const sliders = document.querySelectorAll('.slider'); // выбираем все слайдеры

  sliders.forEach(slider => { // для каждого слайдера
      let currentIndex = 0; // текущий слайд по индексу
      const slides = slider.querySelectorAll('.slide'); // выбираем все слайды
      const prevBtn = slider.querySelector('.prevBtn'); // кнопка "предыдущий" для текущего слайдера
      const nextBtn = slider.querySelector('.nextBtn'); // кнопка "следующий" для текущего слайдера

      function showSlide(index) { // показать слайд по индексу
          slides.forEach((slide, i) => {
              slide.style.display = i === index ? 'block' : 'none'; // показать слайд по индексу
          });
      }

      prevBtn.addEventListener('click', function() { // предыдущий слайд по индексу
          currentIndex = (currentIndex - 1 + slides.length) % slides.length; // индекс предыдущего слайда
          showSlide(currentIndex); // показать предыдущий слайд
      });

      nextBtn.addEventListener('click', function() { // следующий слайд по индексу
          currentIndex = (currentIndex + 1) % slides.length; // индекс следующего слайда
          showSlide(currentIndex); // показать следующий слайд
      });

      showSlide(currentIndex); // показать первый слайд при загрузке
  });
});