const opt = document.querySelector(".sel");
const price = document.querySelector(".text h2");

const quantity = document.querySelector(".quantity");
quantity.addEventListener("input", () => {
  quantity.value = quantity.value.replace("-", "");
});
quantity.addEventListener("focusout", () => {
  if (quantity.value == "" || quantity.value < 1) {
    quantity.value = 1;
  }
});
var output = "{{ ((images.values() | list)[3] * currency)|round(2, 'ceil') }}";
opt.addEventListener("change", () => {
  if (opt.value == "Size: {{ (images.keys() | list)[4] }}") {
    output = "{{ ((images.values() | list)[4] * currency)|round(2, 'ceil') }}";
  } else if (opt.value == "Size: {{ (images.keys() | list)[3] }}") {
    output = "{{ ((images.values() | list)[3] * currency)|round(2, 'ceil') }}";
  }
  price.innerHTML = "{{symbol}}" + " " + output;
});
const buy = document.querySelector(".ADD");
buy.addEventListener("click", () => {
  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "/info",
    data: JSON.stringify({
      name: "{{name}}",
      price: output,
      image: "{{images['path']}}",
      quantity: quantity.value,
    }),
    dataType: "json",
  });
});
