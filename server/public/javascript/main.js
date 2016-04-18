$(document).ready(function() {
  $('.parallax').parallax();
  $("select").material_select();
  $(".button-collapse").sideNav(); // init sidenav bar for mobile

  // Clicking of most of the stream frame
  $(".feed-item").click(function() {
    window.open($(this).attr("data-url"), "_blank");
  });

  $(".ajax-link").click(function() {
    $.post({
      url: $(this).attr("data-route"),
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        'url': $(this).attr("data-url"),
        'named': $(this).attr("data-named"),
        'date': $(this).attr("data-date"),
        'feed': $(this).attr("data-feed")
      }),
      success: function(data, status, jqXHR) {
        Materialize.toast(data, 5000);
      },
      error: function(data, status, jqXHR) {
        console.log(data.responseText);
      }
    });
  });
});
