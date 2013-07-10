var xl;
var current_sender_id = null;
var current_item_id = null;
YUI().use('node', 'event', 'io','json', function (Y) {
    var sender_refresh = function(item_id,sender_id){
        Y.io('/api/thread?item_id='+item_id+'&sender_id='+sender_id,{
                            on:{
                                success:function(code, value){
                                    current_sender_id = sender_id;
                                    Y.all('#main ul li').remove();
                                    var data = Y.JSON.parse(value.responseText).data;
                                    for (var x in data){
                                        //Y.one.('#main ul').append(threadhtml(data[x]);
                                            Y.one('#main ul').append(threadhtml(data[x]));
                                        }
                                        Y.one('#main ul').append(replyBox());
                                        reply_form();
                                    }
                                }
                            });
    };
    var onSenderClick = function(e){
                        var item = e.currentTarget;
                        Y.all('#list .content ul li').removeClass('email-item-selected');
                        if(item.hasClass('no-msg')){
                            return;
                        }
                        item.addClass('email-item-selected');
                        item_id = item.one('input[name="item_id"]').get('value');
                        sender_id = item.one('input[name="sender_id"]').get('value');
                        // console.log(item_id,sender_id);
                        sender_refresh(item_id,sender_id);
                    };
    var reply_form = function(){
        //reply form
        replyForm = Y.one('#reply-form');
        console.log('replyForm');
        console.log(replyForm);
        replyForm.on('submit', function(evt){
                evt.preventDefault();
                console.log('reply form submitted');
                var text_area=Y.one('#reply-form textarea');
                var msg = text_area.get('value');

                var start_reply = function(){
                    text_area.set('disabled',true);
                };
                var complete_reply = function(){
                    // console.log(Y.one('#list .content ul li.email-item-selected'));
                    sender_refresh(current_item_id,current_sender_id);
                };

                console.log('msg = '+msg);
                var cfg = {
                    method: 'POST',
                    data: {
                        'message':msg,
                        'sender_id':current_sender_id,
                        'item_id':current_item_id},
                    on: {
                        start: start_reply(),
                        // complete: complete_reply(),
                        end: function(){
                            Y.all('#list .content ul li').removeClass('email-item-selected');
                            sender_refresh(current_item_id,current_sender_id);
                        }
                    }
                };
                // post msg
                // update UI with new msg
                Y.io('/api/send', cfg);
                console.log('sent');

                });
    };
    function makehtml(msg){
        var html = '<li><div class="email-item ';
        //if(msg.read){
            html+='email-item';
        //}else{
          //  html+='email-item-unread';
        //}
        // html += (msg.read : 'email-item' ? 'email-item-unread');
        html +=' pure-g">\
        <div class="pure-u">\
        <img class="email-avatar" alt="Eric Ferraiuolos avatar" src="http://www.gravatar.com/avatar/'+msg.sender__email+'?s=64" height="64" width="64">\
        </div>\
        \
        <div class="pure-u-3-4">\
        <h5 class="email-name">'+msg.sender__first_name+' '+msg.sender__last_name+' ('+msg.sender__count+') </h5>\
        <h4 class="email-subject">'+msg.item__name+'</h4>\
        <p class="email-desc">\
        price: <strong>$'+ msg.item__price + '</strong> \
        </p>\
        </div>\
        </div> \
        <input type="hidden" name="item_id" value='+msg.item+' />\
        <input type="hidden" name="sender_id" value='+msg.sender+' />\
        </li>';
        return html
    }

    function threadhtml(msg){
        //console.log(msg);
        return '<li class="content pure-g">\
        <div class="email-item pure-g">\
        <div class="pure-u">\
        <img class="email-avatar" src="http://www.gravatar.com/avatar/'+msg.sender__email+'?s=40" height="40" width="40">\
        </div>\
        \
        <div class="pure-u-3-4">\
        <h5 class="email-name">'+msg.sender__first_name+' '+msg.sender__last_name+'</h5>\
        <h6 class="email-date">'+msg.timestamp+' ago</h6>\
        <p class="email-desc msg-text">\
        '+msg.content+'\
        </p>\
        </div>\
        </div>\
        </li>'
    }
    function replyBox(){
        return '<li class="content pure-g">\
    <div class="email-item pure-g">\
        <form id="reply-form" class="pure-form">\
            <fieldset>\
                <div class="pure-control-group">\
                    <textarea id="new_reply"></textarea>\
                </div>\
                <div class="pure-controls">\
                    <button type="submit" class="pure-button pure-button-primary pull-right">Reply</button>\
                </div>\
            </fieldset>\
        </form>\
    </div>\
</li>'
    }
    

var onItemClick = function(e){
    var clcked_item = e.currentTarget;
    var clcked_item_id = clcked_item.one('a').get('name');
    // console.log('id is '+clcked_item_id);
    Y.all('#list .content ul li').remove();
    Y.io(
        '/api/item?id='+clcked_item_id, {
            on: {
                success: function (tx, r) {
                    current_item_id = clcked_item_id;
                    var parsedResponse = null;
                // protected against malformed JSON response
                try {
                    // console.log(r.responseText);
                    parsedResponse = Y.JSON.parse(r.responseText);
                } catch (e) {
                    console.log("JSON Parse failed!");
                    return;
                }
                // console.log('parsedResponse');
                // console.log(parsedResponse.length);
                if(parsedResponse){
                    if(parsedResponse.length == 0){
                        Y.one('#list .content ul').append('\
                            <li class="email-item no-msg"><p>You have not received any messages yet for this item.</p></li>\
                            ');
                    }
                    for (var i in parsedResponse) {
                        // console.log(parsedResponse[i]);
                        Y.one('#list .content ul').append(makehtml(parsedResponse[i]));
                    }
                    
                    Y.one('#list .content ul').delegate('click', onSenderClick, 'li');
                }
            }
        }
    }); // end of io
}

Y.one('#post-items').delegate('click', onItemClick, 'li');
}); //end of YUI