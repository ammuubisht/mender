function mySearchFunction() {
    var input, filter, ul, li, item, i, txtValue;
    input = document.getElementById("autoComplete");
    filter = input.value.toUpperCase();
    ul = document.getElementById("stateList");
    li = ul.getElementsByTagName("li");  for (i = 0; i < li.length; i++) {
      item = li[i];
      txtValue = item.textContent || item.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }