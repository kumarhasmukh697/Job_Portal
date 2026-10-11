/**
 * Job Portal – Light interactivity
 * Only UI helpers (modals, mobile menu, tabs). No data population.
 */

document.addEventListener("DOMContentLoaded", () => {
  // ---------- Mobile Menu ----------
  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileNav = document.getElementById("mobile-nav");

  if (menuBtn && mobileNav) {
    menuBtn.addEventListener("click", () => {
      mobileNav.classList.toggle("open");
      const expanded = mobileNav.classList.contains("open");
      menuBtn.setAttribute("aria-expanded", expanded);
    });
  }

  // ---------- Modals ----------
  // Open any modal via data-modal-target="#modal-id"
  document.querySelectorAll("[data-modal-target]").forEach((trigger) => {
    trigger.addEventListener("click", (e) => {
      e.preventDefault();
      const target = document.querySelector(trigger.dataset.modalTarget);
      if (target) {
        target.classList.add("open");
        document.body.style.overflow = "hidden";
      }
    });
  });

  // Close modal via data-modal-close or clicking overlay
  document.querySelectorAll("[data-modal-close]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const modal = btn.closest(".modal-overlay");
      if (modal) {
        modal.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  });

  // Escape key closes open modal
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const openModal = document.querySelector(".modal-overlay.open");
      if (openModal) {
        openModal.classList.remove("open");
        document.body.style.overflow = "";
      }
    }
  });

  // ---------- Tabs ----------
  document.querySelectorAll("[data-tabs]").forEach((tabContainer) => {
    const buttons = tabContainer.querySelectorAll(".tab-btn");
    const panels = tabContainer.querySelectorAll(".tab-panel");

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetId = btn.dataset.tab;

        buttons.forEach((b) => b.classList.remove("active"));
        panels.forEach((p) => p.classList.remove("active"));

        btn.classList.add("active");
        const panel = tabContainer.querySelector(`#${targetId}`);
        if (panel) panel.classList.add("active");
      });
    });
  });

  // ---------- Simple filter toggle (mobile) ----------
  const filterToggle = document.getElementById("filter-toggle");
  const filterSidebar = document.getElementById("filter-sidebar");

  if (filterToggle && filterSidebar) {
    filterToggle.addEventListener("click", () => {
      filterSidebar.classList.toggle("hidden-mobile");
    });
  }
});
