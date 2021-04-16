
function checkEmailValidity (email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

document.querySelector('select').value = "US";
const labels = document.querySelectorAll('label');

labels.forEach((e) => {
  e.classList.add(e.innerText.replace(":", "").replace(/\s+/g, "").trim());
});

document.querySelector('.Country').style.display = "block";
const inputs = document.querySelectorAll('input');

inputs.forEach((e) => {
  e.addEventListener('input', () => {
    var selected = document.getElementsByClassName(e.getAttribute("placeholder").replace(":", "").replace(/\s+/g, "").trim());
    selected[0].style.display = "block";
  });

  e.addEventListener('focusout', () =>
  {
    if (e.value === "") {
      var selected = document.getElementsByClassName(e.getAttribute("placeholder").replace(":", "").replace(/\s+/g, "").trim());
      selected[0].style.display = "none";
    }
  });
});

const submit = document.querySelector(".pay");
submit.addEventListener("click", () => {
  var allFilled = true;
  const data = document.querySelectorAll("input[type=text], input[type=tel], input[type=number], select");
  const email = document.querySelector("input[name=email]")
  if (!checkEmailValidity(email.value)) {
    allFilled = false;
    email.style.borderColor = "red";
    email.scrollIntoView(false);
  }
  data.forEach((i) => {
    if (i.value == "" && i.name != "Address2") {
      i.style.borderColor = "red";
      allFilled = false;
    }
  });
  if (allFilled) {
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/customer",
      data: JSON.stringify({
        "cus_name": data[0].value, 
        "email": data[1].value,
        "address1": data[2].value,
        "address2": data[3].value,
        "phone": data[4].value,
        "city": data[5].value,
        "postal": data[6].value,
        "state": data[7].value,
        "country": data[8].value
      }),
      dataType: "json"
    });

    var stripe = Stripe('pk_test_51IdTodSIXcXkEUKCUcQmjxWfgpVJKrlVy1TqH1vOjhELy3g2dHDxhtkjo1NrLtqeBdnGlrrpVrQbTxMZk9u8EySd00JG3tKeiR');
    fetch('/create-checkout-session', {
    method: 'POST',
    })
    .then(function(response) {
    return response.json();
    })
    .then(function(session) {
    return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function(result) {
    // If `redirectToCheckout` fails due to a browser or network
    // error, you should display the localized error message to your
    // customer using `error.message`.
    if (result.error) {
        alert(result.error.message);
    }
    })
    .catch(function(error) {
    console.error('Error:', error);
  });
  }
});