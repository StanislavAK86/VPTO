const galleryContainer = document.querySelector(".gallery-container");

const images = document.querySelectorAll(".gallery-image");

const prevButton = document.getElementById("prev-btn");

const nextButton = document.getElementById("next-btn");

let currentImageIndex = 0;

// Функция для отображения картинки

function showImage(index) {
  images.forEach((image, i) => {
    if (i === index) {
      image.style.transform = "scale(1)";
    } else {
      image.style.transform = "scale(0)";
    }
  });
}

// Переключение к предыдущему

function showPreviousImage() {
  currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;

  showImage(currentImageIndex);
}

// Переключение к следующему

function showNextImage() {
  currentImageIndex = (currentImageIndex + 1) % images.length;

  showImage(currentImageIndex);
}

// Слушатели событий для кнопок

prevButton.addEventListener("click", showPreviousImage);

nextButton.addEventListener("click", showNextImage);

// Показываем первую картинку

showImage(currentImageIndex);

// Добавление индикатора

const imageIndicator = document.createElement('div');

imageIndicator.classList.add('image-indicator');

galleryContainer.appendChild(imageIndicator);

function updateImageIndicator() {

imageIndicator.innerHTML = `${currentImageIndex + 1} / ${images.length}`;

}

// Обновление индикатора при переключении

function showPreviousImage() {

currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;

showImage(currentImageIndex);

updateImageIndicator();

}

function showNextImage() {

currentImageIndex = (currentImageIndex + 1) % images.length;

showImage(currentImageIndex);

updateImageIndicator();

}

// Показываем текущее и обновляем индикатор

showImage(currentImageIndex);

updateImageIndicator();