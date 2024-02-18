const chatbotToggler = document.querySelector(".chatbot-toggler");
const iframeContainer = document.querySelector(".iframe-container");

chatbotToggler.addEventListener("click", () => {
    // Toggle the display of the iframe
    const iframe = document.querySelector("iframe");
    iframe.style.display = (iframe.style.display === "none") ? "block" : "none";
});
