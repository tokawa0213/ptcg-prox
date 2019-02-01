$("#draw").click(function () {
    if($("#deck li").length === 0){
        alert("No more card in deck")
    }else{
        //change top deck list
        var top_card = $("#deck li").eq(0);
        top_card.remove();
        $("#hand ul").append(top_card)
        update_card_draggable()
    }
});
$("#shuffle").click(function (){
    var arr = [];
    $("#deck li").each(function() {
        arr.push($(this).html());
    });
    arr.sort(function() {
        return Math.random() - Math.random();
    });
    $("#deck").empty();
    for(var i=0; i < arr.length; i++) {
        $("#deck").append('<li>' + arr[i] + '</li>');
    }
    alert("デッキがシャッフルされました")
});

$("#deck_position").click(function (){
    //slideup slide down
    $("#deck").slideToggle();
    $("#trash").slideUp();
    $("#lost").slideUp();
});
$("#trash_position").click(function (){
    $("#trash").slideToggle();
    $("#deck").slideUp();
    $("#lost").slideUp();
});
$("#lost_position").click(function (){
    $("#lost").slideToggle();
    $("#trash").slideUp();
    $("#deck").slideUp();
});
