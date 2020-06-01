function selectcapture(gallery_thumbnail){
    console.log(`Selecting capture: ${gallery_thumbnail}`);
    thumbnail_image = $(gallery_thumbnail).find('.thumbnail-image');
    thumbnail_image.removeClass('deselected-thumbnail');
    thumbnail_image.addClass('selected-thumbnail');
}