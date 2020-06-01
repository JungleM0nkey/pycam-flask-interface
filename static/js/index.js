function selectcapture(gallery_thumbnail){
    console.log(`Selecting capture: ${gallery_thumbnail}`);
    $('.selected-thumbnail').addClass('deselected-thumbnail');
    $('.selected-thumbnail').removeClass('selected-thumbnail');
    thumbnail_image = $(gallery_thumbnail).find('.thumbnail-image');
    thumbnail_image.removeClass('deselected-thumbnail');
    thumbnail_image.addClass('selected-thumbnail');
    thumbnail_src = thumbnail_image.attr('src');
    $('#selected-capture').attr('src',thumbnail_src)
}