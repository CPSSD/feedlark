$(document).ready(function() {
  $('.parallax').parallax();
  $("select").material_select();
  $(".button-collapse").sideNav(); // init sidenav bar for mobile

  $(".ajax-link").click(function() {
    $.post({
      url: $(this).attr("data-route"),
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        'url': $(this).attr("data-url"),
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

  function change_page(page) {
    $("[name='page']").val(page);
    $("form").submit();
  }
});
