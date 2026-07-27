const themeButton = document.getElementById("themeToggle");

themeButton.addEventListener("click", () => {

    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){

        themeButton.textContent = "☀";

    }

    else{

        themeButton.textContent = "🌙";

    }

});
function toggleSummary(button){

    const content = button.nextElementSibling;

    content.classList.toggle("show");

    if(content.classList.contains("show")){

        button.textContent = "▲ Hide AI Summary";

    }
    else{

        button.textContent = "▼ View AI Summary";

    }

}