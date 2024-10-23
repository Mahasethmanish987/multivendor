let autocomplete;

function initAutoComplete(){
    autocomplete=new google.maps.places.Autocomplete(
        document.getElementById('id_address'),{
            types:['geocode','establishment'],
            componentRestrictions:{'country':['NP']},
        }
    )
    autocomplete.addListener('place_changed',onPlacedChanged)
}

function onPlacedChanged(){
    var place=autocomplete.getPlace();
    if(!place.geometry){
        document.getElementById('id_address').placeholder='start typing...'

    }
    else{
        // console.log('place name=>',place.name)
    }

    // console.log(place)
    var geocoder =new google.maps.Geocoder()
    var address=document.getElementById('id_address').value
    console.log(address)
    geocoder.geocode({'address':address},function(results,status){
        if(status==google.maps.GeocoderStatus.OK){
            var latitude=results[0].geometry.location.lat();
            
            var longitude=results[0].geometry.location.lng();
            $('#id_latitude').val(latitude)
            $('#id_longitude').val(longitude)
            
            
            $('#id_address').val(address)
            
        }
    })
    console.log(place.address_components)
    for(var i=0 ;i<place.address_components.length;i++)
    {
        for(var j=0 ;j<place.address_components[i].types.length ;j++)
        {
            if(place.address_components[i].types[j]=='country'){
                $('#id_country').val(place.address_components[i].long_name)
            }
            if(place.address_components[i].types[j]=='administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name)
            }
            if(place.address_components[i].types[j]=='postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name)
            }


        }
    }

}