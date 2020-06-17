function selectcapture(gallery_thumbnail){
    console.log(`Selecting capture: ${gallery_thumbnail}`);
    $('.fa-video').css('color', 'rgba(0, 0, 0, 0.712)')
    $('.selected-thumbnail').addClass('deselected-thumbnail');
    $('.selected-thumbnail').removeClass('selected-thumbnail');
    thumbnail_image = $(gallery_thumbnail).find('.thumbnail-image');
    thumbnail_image.removeClass('deselected-thumbnail');
    thumbnail_image.addClass('selected-thumbnail');
    thumbnail_src = thumbnail_image.attr('src');
    thumbnail_date = thumbnail_image.attr('id')
    $('#selected-capture').attr('src',thumbnail_src) //change selected image source
    $('#selected-capture-date').text(`${thumbnail_date}`) //change date under selected image
}

function changetheme(theme){
    if(theme == 'dark'){
        $('body').css('background-image','url(../static/images/invertedbg.png)')
        $('label').css('color','rgba(255, 255, 255, 0.74)')
        $('#index-title').css('color','white')
        $('#archive-title').css('color','rgba(255, 255, 255, 0.561)')
        $('#settings-title').css('color','rgba(255, 255, 255, 0.561)')
        $('#selected-capture-date').css('color','rgba(255, 255, 255, 0.74)')
        $('.thumbnail-date').css('color','rgba(255, 255, 255, 0.74)')
        $('#change-theme').css('color','white')
    }else{
        $('body').css('background-image','url(../static/images/bg.png)')
        $('label').css('color','black')
        $('#index-title').css('color','black')
        $('#archive-title').css('color','rgba(0, 0, 0, 0.431)')
        $('#settings-title').css('color','rgba(0, 0, 0, 0.431)')
        $('#selected-capture-date').css('color','black')
        $('.thumbnail-date').css('color','black')
        $('#change-theme').css('color','rgba(0, 0, 0, 0.712)')
    }
    savetheme(theme)
}

function savetheme(theme){
    //document.cookie = `theme=${theme}; expires=Thu, 31 Dec 2099 12:00:00 UTC`
    Cookies.set('theme', theme);
}

function gettheme(){
    //theme = ("; "+document.cookie).split("; theme=").pop().split(";").shift();
    theme = Cookies.get('theme');
    if (!theme){
        theme = 'light'
    }
    return theme
}