window.addEventListener('load', () => {
    const containers = document.querySelectorAll('.container-year');
    let maxHeight = 0;
    
    containers.forEach(c => {
      c.style.height = 'auto';  // reset height
      if (c.offsetHeight > maxHeight) {
        maxHeight = c.offsetHeight;
      }
    });
  
    containers.forEach(c => {
      c.style.height = maxHeight + 'px';
    });
  });
  


  const btn = document.getElementById("backToTopBtn");
  window.onscroll = function () {
      btn.style.display = window.pageYOffset > 300 ? "block" : "none";
  };

  function scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
  }