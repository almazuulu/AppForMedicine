
var dataObject = JSON.parse(dataJSON);
var listItemString = $('#listItem').html();

dataObject.forEach(buildNewList);

function buildNewList(item, index) {
  var listItem = $('<li>' + listItemString + '</li>');
  var listItemTitle = $('.title', listItem);
  listItemTitle.html(item.FeeType);
  var listItemAmount = $('.amount', listItem);
  listItemAmount.html(item.FeeAmount);
  var listItemDesc = $('.description', listItem);
  listItemDesc.html(item.FeeDescription);
  $('#dataList').append(listItem);
}