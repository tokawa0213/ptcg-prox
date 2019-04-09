$("#draw").click(function () {
    if($("#deck li").length === 0){
        toastr.info("デッキにカードがありません")
    }else{
        //change top deck list
        var top_card = $("#deck li").eq(0);
        top_card.remove();
        $("#hand ul").append(top_card);
        update_card_draggable();
        toastr.info("カードを引きました")
    }
});
$("#return").click(function () {
    if($("#hand li").length === 0){
        toastr.info("手札にカードがありません")
    }else{
        //change top deck list
        var left_card = $("#hand li").eq(0);
        left_card.remove();
        $("#deck").prepend(left_card);
        update_card_draggable();
        toastr.info("カードを戻しました")
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
    toastr.info("デッキがシャッフルされました")
});
$("#coin").click(function (){
    coinr_result = Math.random()
    if(coinr_result > 0.5){
        toastr.info("コイン結果：表")
    }else{
        toastr.info("コイン結果：裏")
    }
});
$("#deck_position").click(function (){
    $("#deck li").each(function(index,element){$(element).show()});
    if($("#deck").css("display") === "none"){
        toastr.info("デッキをサーチします");
    }else{
        toastr.info("デッキを閉じます");
    }
    $("#deck").slideToggle();
    $("#trash").slideUp();
    $("#lost").slideUp();
});
$("#trash_position").click(function (){
    if($("#trash").css("display") === "none"){
        toastr.info("トラッシュを参照します");
    }else{
        toastr.info("トラッシュを閉じます");
    }
    $("#trash").slideToggle();
    $("#deck").slideUp();
    $("#lost").slideUp();
});
$("#lost_position").click(function (){
    if($("#lost").css("display") === "none"){
        toastr.info("ロストゾーンを参照します");
    }else{
        toastr.info("ロストゾーンを閉じます");
    }
    $("#lost").slideToggle();
    $("#trash").slideUp();
    $("#deck").slideUp();
});
$("[id^='side-']").click(function (){
    var side_position = $(this);
    var side_card = side_position.children().filter(
        function(index){
            return $.isNumeric($(this).attr("id"));
        }
        );
    var side_back_card = $(this).children(".back_card");
    if(side_card.prop("outerHTML") != null){
        side_card.show();
        side_card.remove();
        side_back_card.hide();
        $("#hand ul").append("<li>"+side_card.prop("outerHTML")+"</li>");
        update_card_draggable();
    }
});
$("#exe_top_card_num").click(function(){
    var card_num = Number($("#top_card_num").prop("value"));
    if($("#deck li").length < card_num){
        toastr.info("指定枚数が大き過ぎます")
    }else{
        toastr.info("デッキの上から"+card_num+"枚表示");
        $("#deck li").each(
            function(index,element){
                if(index >= card_num) {
                    $(element).hide()
                }
            }
            );
        $("#deck").slideToggle();
        update_card_draggable();
    }
});