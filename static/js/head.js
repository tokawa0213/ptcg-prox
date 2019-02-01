var update_card_draggable = function(){
$(".card").draggable({
    start:function(){
        drag_object = $(this);
    },
    appendTo: "body",
    helper: "clone"
});
};

window.onload = function(){
for (var card_num =0; card_num < hand.length;card_num++){
    $("#hand ul").append("<li><img src=static/imdir/"+hand[card_num]+".jpg class=\"card\" id="+card_num.toString()+"></li>")
}
for (var deck_c_num =7; deck_c_num < deck.length;deck_c_num++){
    $("#deck").append("<li><img src=static/imdir/"+deck[deck_c_num]+".jpg class=\"card\" id="+deck_c_num.toString()+"></li>")
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

    },
});

$(".drop_disappear").droppable({
    drop: function(){
        drag_object_id = drag_object.attr("id");
        drag_object_parent_id = drag_object.parents("div").attr("id");
        if ($(this).attr("id") !== drag_object_parent_id){
            //remove from ul
            drag_object.removeClass("style");
            var drop_id = "#" + $(this).attr("id").toString().replace("_position","");
            var appending_line = drag_object.parent().html();
            $("#"+drag_object_parent_id.split(" ")[0] + " li img[id=" + drag_object_id+"]").remove();
            $("#"+drag_object_parent_id.split(" ")[0] + " li:empty").remove();
            $(drop_id).prepend("<li>" + appending_line + "</li>");
            update_card_draggable();
        }
    },
});
};