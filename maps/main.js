window.onload = init;


function init(){
    const map=new ol.Map({
        view: new ol.View({
            center: [0,0],
            zoom:2
        }),
        layers:[
            new ol.Layer.Vector({
                protocol: new ol.Protocol.HTTP({
                    url: "/map.osm",   //<-- relative or absolute URL to your .osm file
                    format: new ol.Format.OSM()
                })
            })
        ],
        target: 'js-map'
    })

//     var layer = new ol.Layer.Vector("Polygon", {
//         strategies: [new ol.Strategy.Fixed()],
//         protocol: new ol.Protocol.HTTP({
//             url: "map.osm",   //<-- relative or absolute URL to your .osm file
//             format: new ol.Format.OSM()
//         }),
//         projection: new ol.Projection("EPSG:4326")
//     })

//     map.addLayers([layer])
}