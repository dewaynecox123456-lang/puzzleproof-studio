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
