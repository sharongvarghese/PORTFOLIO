
// Minimal JS: activate current nav link based on scroll position
document.addEventListener("DOMContentLoaded", () => {
  const sections = [...document.querySelectorAll("main section[id]")];
  const navLinks = [...document.querySelectorAll(".navbar .nav-link")];

  const setActive = () => {
    let fromTop = window.scrollY + 120; // account for fixed navbar
    let current = sections.findLast(sec => sec.offsetTop <= fromTop);
    navLinks.forEach(link => link.classList.remove("active"));
    if (current) {
      const active = navLinks.find(a => a.getAttribute("href") === `#${current.id}`);
      if (active) active.classList.add("active");
    }
  };

  setActive();
  window.addEventListener("scroll", setActive);
});
