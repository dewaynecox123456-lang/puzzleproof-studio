const externalLinks = document.querySelectorAll('a[href^="http"]');

externalLinks.forEach((link) => {
  link.setAttribute("target", "_blank");
});

const forms = document.querySelectorAll("form[data-netlify]");

forms.forEach((form) => {
  form.addEventListener("submit", () => {
    const button = form.querySelector("button");
    if (button) {
      button.textContent = "Sending request...";
    }
  });
});

const carousels = document.querySelectorAll("[data-carousel]");

carousels.forEach((carousel) => {
  const slides = Array.from(carousel.querySelectorAll("[data-slide]"));
  const dots = Array.from(carousel.querySelectorAll("[data-carousel-dot]"));
  const previous = carousel.querySelector("[data-carousel-prev]");
  const next = carousel.querySelector("[data-carousel-next]");
  let currentIndex = 0;

  const showSlide = (nextIndex) => {
    currentIndex = (nextIndex + slides.length) % slides.length;

    slides.forEach((slide, index) => {
      const isActive = index === currentIndex;
      slide.classList.toggle("is-active", isActive);
      slide.hidden = !isActive;
    });

    dots.forEach((dot, index) => {
      const isActive = index === currentIndex;
      dot.classList.toggle("is-active", isActive);
      if (isActive) {
        dot.setAttribute("aria-current", "true");
      } else {
        dot.removeAttribute("aria-current");
      }
    });
  };

  previous?.addEventListener("click", () => showSlide(currentIndex - 1));
  next?.addEventListener("click", () => showSlide(currentIndex + 1));

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => showSlide(index));
  });
});
