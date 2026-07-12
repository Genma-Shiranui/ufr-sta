// ── Navbar toggle mobile ───────────────────────────────
const toggle = document.getElementById("navToggle");
const links = document.getElementById("navLinks");

if (toggle && links) {
  toggle.addEventListener("click", () => {
    links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", links.classList.contains("open"));
  });

  // Fermer le menu en cliquant ailleurs
  document.addEventListener("click", (e) => {
    if (!toggle.contains(e.target) && !links.contains(e.target)) {
      links.classList.remove("open");
    }
  });
}

// ── Lien actif au scroll ───────────────────────────────
// (optionnel pour les pages à section unique)
const navLinks = document.querySelectorAll(".nav-link");
navLinks.forEach((link) => {
  if (link.href === window.location.href) {
    link.classList.add("active");
  }
});
