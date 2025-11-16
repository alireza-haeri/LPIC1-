/**
 * Custom JavaScript for LPIC-1 Persian Documentation
 * Enhances user experience and adds interactive features
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('LPIC-1 Persian Documentation loaded successfully');
  
  // Initialize features
  initSmoothScroll();
  initCodeCopyButtons();
  initBackToTop();
  initExternalLinks();
  initSearchEnhancements();
  
});

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // Update URL without scrolling
        history.pushState(null, null, targetId);
      }
    });
  });
}

/**
 * Enhance code copy functionality
 */
function initCodeCopyButtons() {
  // Add copy button animation
  document.querySelectorAll('.md-clipboard').forEach(button => {
    button.addEventListener('click', function() {
      const icon = this.querySelector('.md-clipboard__icon');
      if (icon) {
        icon.style.transform = 'scale(1.2)';
        setTimeout(() => {
          icon.style.transform = 'scale(1)';
        }, 200);
      }
    });
  });
}

/**
 * Back to top button functionality
 */
function initBackToTop() {
  const backToTopButton = document.querySelector('.md-top');
  
  if (backToTopButton) {
    // Show/hide based on scroll position
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 300) {
        backToTopButton.style.opacity = '1';
        backToTopButton.style.visibility = 'visible';
      } else {
        backToTopButton.style.opacity = '0';
        backToTopButton.style.visibility = 'hidden';
      }
    });
    
    // Smooth scroll to top
    backToTopButton.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
}

/**
 * Mark external links and open in new tab
 */
function initExternalLinks() {
  const domain = window.location.hostname;
  
  document.querySelectorAll('a[href^="http"]').forEach(link => {
    const linkDomain = new URL(link.href).hostname;
    
    if (linkDomain !== domain) {
      // Mark as external
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
      
      // Add external link icon
      if (!link.querySelector('.external-link-icon')) {
        const icon = document.createElement('span');
        icon.className = 'external-link-icon';
        icon.innerHTML = ' ↗';
        icon.style.fontSize = '0.8em';
        icon.style.opacity = '0.6';
        link.appendChild(icon);
      }
    }
  });
}

/**
 * Search enhancement features
 */
function initSearchEnhancements() {
  const searchInput = document.querySelector('.md-search__input');
  
  if (searchInput) {
    // Add Persian keyboard support hints
    searchInput.setAttribute('placeholder', 'جستجو... (Ctrl+K)');
    
    // Keyboard shortcut (Ctrl+K or Cmd+K)
    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
      }
    });
    
    // Clear search on Escape
    searchInput.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        this.value = '';
        this.blur();
      }
    });
  }
}

/**
 * Add reading progress indicator
 */
function initReadingProgress() {
  const progressBar = document.createElement('div');
  progressBar.id = 'reading-progress';
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(to left, var(--md-primary-fg-color), var(--md-accent-fg-color));
    transform-origin: right;
    transform: scaleX(0);
    z-index: 1000;
    transition: transform 0.1s ease;
  `;
  document.body.appendChild(progressBar);
  
  window.addEventListener('scroll', function() {
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.pageYOffset / windowHeight);
    progressBar.style.transform = `scaleX(${scrolled})`;
  });
}

// Initialize reading progress
initReadingProgress();

/**
 * Add print-friendly enhancements
 */
window.addEventListener('beforeprint', function() {
  // Expand all collapsed sections before printing
  document.querySelectorAll('details').forEach(detail => {
    detail.setAttribute('open', '');
  });
});

/**
 * Keyboard navigation enhancement
 */
document.addEventListener('keydown', function(e) {
  // Next/Previous page navigation with arrow keys
  if (e.altKey) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      const direction = e.key === 'ArrowRight' ? '.md-footer__link--prev' : '.md-footer__link--next';
      const navLink = document.querySelector(direction);
      if (navLink) {
        e.preventDefault();
        navLink.click();
      }
    }
  }
});

/**
 * Add copy notification
 */
function showCopyNotification(message) {
  const notification = document.createElement('div');
  notification.textContent = message || 'کپی شد!';
  notification.style.cssText = `
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: var(--md-primary-fg-color);
    color: white;
    padding: 12px 24px;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 9999;
    animation: slideUp 0.3s ease;
    font-family: Vazirmatn, sans-serif;
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideDown 0.3s ease';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 2000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideUp {
    from {
      transform: translateX(-50%) translateY(100px);
      opacity: 0;
    }
    to {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }
  }
  
  @keyframes slideDown {
    from {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }
    to {
      transform: translateX(-50%) translateY(100px);
      opacity: 0;
    }
  }
  
  .md-clipboard:active {
    transform: scale(0.95);
  }
`;
document.head.appendChild(style);

/**
 * Table of contents scroll spy
 */
function initTOCScrollSpy() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const id = entry.target.getAttribute('id');
      const tocLink = document.querySelector(`.md-nav__link[href="#${id}"]`);
      
      if (tocLink) {
        if (entry.isIntersecting) {
          tocLink.classList.add('md-nav__link--active');
        } else {
          tocLink.classList.remove('md-nav__link--active');
        }
      }
    });
  }, {
    rootMargin: '-80px 0px -80% 0px'
  });
  
  // Observe all headings
  document.querySelectorAll('h2[id], h3[id]').forEach(heading => {
    observer.observe(heading);
  });
}

// Initialize TOC scroll spy
if (document.querySelector('.md-nav--secondary')) {
  initTOCScrollSpy();
}

// Log initialization complete
console.log('All custom scripts initialized successfully');
