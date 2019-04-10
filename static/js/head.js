/*
TODO:
1. Realize Energy attachment
2. Click to take side
3. Easy macro function : Switch
4. See only top n cards
5. css settings (especially font size)
6. Change view (include deck url in url)
7. Damage counters Sleep
*/

var drag_object,drag_object_id,drag_object_parent_id;

var update_card_draggable = function(){
$(".card").draggable({
    start:function(){
        drag_object = $(this);
    },
    appendTo: "body",
    helper: "clone",
    scroll: false
});
};

toastr.options = {
  "closeButton": true,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-left",
  "preventDuplicates": false,
  "onclick": null,
  "showEasing": "swing",
    "timeOut": 1000,
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
};

window.onload = function(){
for (var card_num =0; card_num < hand.length;card_num++){
    $("#hand ul").append("<li><img src=static/imdir/"+hand[card_num]+".jpg class=\"card\" id="+card_num.toString()+"></li>")
}
for (var card_num =0; card_num < deck.length;card_num++){
    $("#deck").append("<li><img src=static/imdir/"+deck[card_num]+".jpg class=\"card\" id="+(hand.length+card_num).toString()+"></li>")
}
for (var card_num =0; card_num < side.length;card_num++){
    $("#side-"+(card_num+1).toString()+"_position").append("<img hidden src=static/imdir/"+side[card_num]+".jpg class=\"card\" id="+(deck.length+hand.length+card_num).toString()+">")
}
// if dropped in drop position, add html to the parent
// else, add it back to the original position

update_card_draggable();

$(".drop").droppable({
    drop: function(){
        drag_object_id = drag_object.attr("id");
        drag_object_parent_id = drag_object.parents("div").attr("id");
        if ($(this).attr("id") !== drag_object_parent_id){
            var appending_line = drag_object.parent().html();
            $("#"+drag_object_parent_id.split(" ")[0] + " li img[id=" + drag_object_id+"]").remove();
            $("#"+drag_object_parent_id.split(" ")[0] + " li:empty").remove();
            $(this).append("<li>" + appending_line + "</li>");
            update_card_draggable();
        }
        $(this).css('z-index', '10');
        $(this).css('background-color', 'rgb(250,219,218,0)')
    },
    over: function(){
        $(this).css('background-color', 'rgb(250,219,218,0.7)')
    },
    out: function(){
        $(this).css('background-color', 'rgb(250,219,218,0)')
    }
});

$(".drop_side").droppable({
    drop: function(){
        drag_object_id = drag_object.attr("id");
        drag_object_parent_id = drag_object.parents("div").attr("id");
        if ($(this).attr("id") !== drag_object_parent_id){
            var appending_line = drag_object.parent().html();
            $("#"+drag_object_parent_id.split(" ")[0] + " li img[id=" + drag_object_id+"]").remove();
            $("#"+drag_object_parent_id.split(" ")[0] + " li:empty").remove();
            $(this).append(appending_line);
            $(this).children(".card").hide();
            $(this).children(".back_card").show();
            update_card_draggable();
        }
        $(this).css('z-index', '10');
        $(this).css('background-color', 'rgb(250,219,218,0)')
    },
    over: function(){
        $(this).css('background-color', 'rgb(250,219,218,0.7)')
    },
    out: function(){
        $(this).css('background-color', 'rgb(250,219,218,0)')
    }
});

$(".drop_sub").droppable({
    drop: function(){
        drag_object_id = drag_object.attr("id");
        drag_object_parent_id = drag_object.parents("div").attr("id");
        if ($(this).attr("id") !== drag_object_parent_id){
            var appending_line = drag_object.parent().html();
            $("#"+drag_object_parent_id.split(" ")[0] + " li img[id=" + drag_object_id+"]").remove();
            $("#"+drag_object_parent_id.split(" ")[0] + " li:empty").remove();
            $(this).append("<li>" + appending_line + "</li>");
            update_card_draggable();
        }
        $(this).css('background-color', 'rgb(250,219,218,0)')
        $(this).css('z-index', '5');
    },
    over: function(){
        $(this).css('background-color', 'rgb(249,250,217,0.7)')
    },
    out: function(){
        $(this).css('background-color', 'rgb(250,219,218,0)')
    }
});

$(".drop_disappear").droppable({
    drop: function(){
        drag_object_id = drag_object.attr("id");
        drag_object_parent_id = drag_object.parents("div").attr("id");
        if ($(this).attr("id") !== drag_object_parent_id){
            //Is the below line working ?
            drag_object.removeClass("style");
            drag_object.removeClass("z-index");
            var drop_id = "#" + $(this).attr("id").toString().replace("_position","");
            var appending_line = drag_object.parent().html();
            $("#"+drag_object_parent_id.split(" ")[0] + " li img[id=" + drag_object_id+"]").remove();
            $("#"+drag_object_parent_id.split(" ")[0] + " li:empty").remove();
            if(drop_id.toString() !== "#hand"){
                $(drop_id).prepend("<li>" + appending_line + "</li>");
            }else{
                $(drop_id + " ul").prepend("<li>" + appending_line + "</li>");
            }
            update_card_draggable();
        }
        $(this).css('background-color', 'rgb(250,219,218,0)')
    },
    over: function(){
        $(this).css('background-color', 'rgb(250,219,218,0.7)')
    },
    out: function(){
        $(this).css('background-color', 'rgb(250,219,218,0)')
    }
});
};

$(document).ready(function(){
    var orientation = window.orientation;
    var noMoreAlert = false;
    if (orientation === 0) {
        if(noMoreAlert===false){
            if(confirm("本アプリは、横向きでの利用を推奨しています。\nこれ以上このメッセージを表示しない場合は「OK」を選択して下さい。")){
                noMoreAlert = true;
            }
        }
    }
});