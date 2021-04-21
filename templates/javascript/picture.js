const opt = document.querySelector("#size");
const price = document.querySelector(".text h2");
const frame = document.querySelector("#frame");

const quantity = document.querySelector(".quantity");
quantity.addEventListener("input", () => {
  quantity.value = quantity.value.replace(".", "");
});
quantity.addEventListener("focusout", () => {
  if (
    quantity.value == "" ||
    quantity.value < 1 ||
    quantity.value.includes(".")
  ) {
    quantity.value = 1;
  }
});

$.ajax({
  type: "POST",
  contentType: "application/json; charset=utf-8",
  url: "/info",
  data: JSON.stringify({
    request: "setup",
    name: "{{name}}",
    image: "{{images['path']}}",
  }),
  dataType: "json",
});

function sendInfo() {
  return new Promise(function (resolve, reject) {
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/info",
      data: JSON.stringify({
        request: "Variants",
        name: "{{name}}",
        quantity: quantity.value,
        size: opt.value.split(": ")[1],
        frame: frame.value.split(": ")[1],
      }),
      success: (response) => {
        output = response["price"];
        resolve(output);
      },
      dataType: "json",
    });
  });
}

document.querySelectorAll("select, .quantity").forEach((i) => {
  i.addEventListener("change", () => {
    sendInfo().then((output) => {
      console.log(output);
      price.innerHTML = "{{symbol}}" + " " + output.toString();
    });
  });
});

const buy = document.querySelector(".ADD");
buy.addEventListener("click", () => {
  sendInfo().then((output) => {
    window.location.href = "/customer";
  });
});
