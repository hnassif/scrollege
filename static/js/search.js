var i_am=null, category= null;

$('#type-dropdown-ul').click(function(evt){
    var target = $(evt.target);
    console.log(target.html());
    // i_am = target.html();
    //set 
    $('#type-dropdown').addClass('hasFilter').html(target.html()+'<b class="caret"></b>');
    $('#filter-need_or_sold').val(target.html());

});

$('#category-dropdown-ul').click(function(evt){
    var target = $(evt.target);
    console.log(""+ target.html()+' has been clicked');
    $('#category-dropdown').addClass('hasFilter').html(target.html()+'<b class="caret"></b>');
    $('#filter-category').val(target.html());
});
