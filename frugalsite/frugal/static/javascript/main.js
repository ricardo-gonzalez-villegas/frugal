const url = window.location.href;
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const favoritesResults = document.getElementById("favorites-results");
const searchCSFR = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const resultsCSFR = document.getElementsByName("csrfmiddlewaretoken")[1].value;

const sendSearchData = (search_param) => {
  $.ajax({
    type: "POST",
    url: "favorites",
    data: {
      csrfmiddlewaretoken: searchCSFR,
      search_param: search_param,
    },
    success: (res) => {
      favoritesResults.innerHTML = res["html_from_view"];
    },
    error: (res) => {
      console.log(res);
    },
  });
};

const deleteFavorite = (search_param, favorite_id) => {
  $.ajax({
    type: "POST",
    url: "favorites/" + favorite_id + "/delete",
    data: {
      csrfmiddlewaretoken: resultsCSFR,
      favorite_id: favorite_id,
      search_param: search_param,
    },
    success: (res) => {
      favoritesResults.innerHTML = res["html_from_view"];
    },
    error: (res) => {
      console.log(res);
    },
  });
};

searchInput.addEventListener("keyup", (e) => {
  sendSearchData(e.target.value);
});

favoritesResults.addEventListener("click", (e) => {
  deleteFavorite(searchInput.value, e.target.value);
});
