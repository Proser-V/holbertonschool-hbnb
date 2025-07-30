// Wait until the full HTML document is loaded
document.addEventListener("DOMContentLoaded", function () {
    // Select the overlay and the image on the overlay
    const overlay = document.getElementById("lightbox-overlay");
    const overlayImg = document.getElementById("lightbox-img");

    // For each photo, link the overlay image with the gallery image, then show the overlay and the image
    document.querySelectorAll(".photo-gallery img").forEach(photo => {
        photo.addEventListener("click", function () {
        overlayImg.src = this.src;
        overlay.classList.remove("hidden");
        });
    });
    // Overlay and photo disapear on click on overlay or image
    overlay.addEventListener("click", function (e) {
        if (e.target === overlay || e.target === overlayImg) {
        overlay.classList.add("hidden");
        overlayImg.src = "";
        }
    });
});
