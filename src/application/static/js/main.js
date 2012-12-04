var Utils = {
    renderFieldErrorTooltip: function (selector, msg, placement) {
        var elem;
        if (typeof placement === 'undefined') {
            placement = 'right'; // default to right-aligned tooltip
        }
        elem = $(selector);
        elem.tooltip({'title': msg, 'trigger': 'manual', 'placement': placement});
        elem.tooltip('show');
        elem.addClass('error');
        elem.on('focus click', function(e) {
            elem.removeClass('error');
            elem.tooltip('hide');
        });
    }
};

/* Your custom JavaScript here */

function loadExternal(url, callback) {
    var container = $('#external .frame');
    container.empty();

    var frame = $('<iframe />', {
        name: 'frame1',
        id: 'frame1',
        src: url
    });
    container.append(frame);

    frame.onload = callback;
}

$(document).ready(function() {
    $('#slides').superslides({
        play: false,
        slide_speed: 'fast',
        pagination: true,
        hashchange: true
    });

    $('.entries li').on('click', 'a.link.title', function(event) {
        event.preventDefault();

        $('#external').show();
        $('.slides-pagination, .slides-navigation').hide();
        $('#slides').animate({
            height: '100px',
            opacity: 0.25,
        }, 800, function() {
        });

        loadExternal(this.href, function() {
            console.log('loaded');
        });
    });

    $('#external').on('click', 'a.close', function(event) {
        $('#slides').show();
        $('#slides').animate({
            height: '100%',
            opacity: 1
        }, 800, function() {
            $('#external').hide();
        });

        $('.slides-pagination, .slides-navigation').show();
    });
});

