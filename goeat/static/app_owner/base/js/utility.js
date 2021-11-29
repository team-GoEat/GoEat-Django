function inputPhoneNumber(value) {
  let number = value.replace(/[^0-9]/g, "");
  let phone = "";

  if (number.length < 4) { return number; }
  else if (number.length < 7) {
    phone += number.substr(0, 3);
    phone += "-"; phone += number.substr(3);
  }
  else if (number.length < 11) {
    phone += number.substr(0, 3);
    phone += "-"; phone += number.substr(3, 3);
    phone += "-"; phone += number.substr(6);
  } else {
    phone += number.substr(0, 3);
    phone += "-"; phone += number.substr(3, 4);
    phone += "-"; phone += number.substr(7);
  }
  return phone;
}
function inputDateNumber(value) {
  let number = value.replace(/[^0-9]/g, "");
  let phone = "";

  if (number.length < 3) { return number; }
  else if (number.length < 4) {
    phone += number.substr(0, 2);
    phone += "."; phone += number.substr(2);
  }
  else if (number.length < 6) {
    phone += number.substr(0, 2);
    phone += "."; phone += number.substr(2, 2);
    phone += "."; phone += number.substr(4);
  }
  else {
    phone += number.substr(0, 2);
    phone += "."; phone += number.substr(2, 2);
    phone += "."; phone += number.substr(4);
  }
  return phone;
}