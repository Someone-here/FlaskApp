const navbar = document.querySelectorAll("#navigation li");
const pic = document.querySelectorAll(".pic");
const all = document.querySelector("#All");

navbar.forEach((i) => {
    i.addEventListener(("click"), () => {
        pic.forEach((j) => {
            var category = $(j).attr("class").split(" ")[1];
            if (category != i.innerHTML) {
                j.style.display = "none";
            }
            else {
                j.style.display = "flex";
            }
        });
    });
});

all.addEventListener("click", () => {
    pic.forEach((o) => {
        o.style.display = "flex";
    });
    });