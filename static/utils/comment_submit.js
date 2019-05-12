// 禁止频繁评论
const submit_comment = (url) => {
    $('#on_submit').attr('disabled', 'disabled').empty().append('发布中.. ').append(
        '<span class="spinner-border spinner-border-sm text-light" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</span>'
    );
    $.get(url, function (result) {
        if (result >= 10) {
            layer.msg('您评论得太频繁了。\n过几分钟再试试吧~');
            $('#on_submit').removeAttr('disabled').empty().append('重新发布');
        } else {
            $('#comment_submit').trigger('click');
        }
    });
};