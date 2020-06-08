function selectcapture(gallery_thumbnail){
    console.log(`Selecting capture: ${gallery_thumbnail}`);
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