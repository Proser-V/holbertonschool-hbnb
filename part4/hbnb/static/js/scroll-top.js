// Select the button with id "scrollToTopBtn"
const scrollBtn = document.getElementById("scrollToTopBtn");

// Make the button appears only when we scroll
window.onscroll = function() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollBtn.style.display = "block";
    } else {
        scrollBtn.style.display = "none";
    }
};

// Going to the top of the page on click
scrollBtn.onclick = function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
};
