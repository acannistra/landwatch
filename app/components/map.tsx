import React, { useRef, useState } from "react";
import ReactMapGL, { ViewState } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';


interface IProps { }

export default function MapRT({ }: IProps) {
    const [viewport, setViewport] = useState<ViewState>({
        latitude: 41,
        longitude: -71,
        zoom: 10
    });

    return (
        <ReactMapGL
            {...viewport}
            mapboxAccessToken="pk.eyJ1IjoiYWNhbm5pc3RyYSIsImEiOiJjbGFlaW9xMTQwdTlrM3ZxeWFuOHNoY2E2In0.2RqODcSl9BH9FO54PlDzCg"
            style={{
                width: "100%", minHeight: "250px"
            }}
            onMove={evt => setViewport(evt.viewState)}
            mapStyle="mapbox://styles/mapbox/streets-v9"

        ></ReactMapGL>
    )
};