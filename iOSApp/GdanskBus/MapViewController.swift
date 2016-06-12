//
//  MapViewController.swift
//  GdanskBus
//
//  Created by Sungwoo on 6/12/16.
//  Copyright © 2016 Kevin Studio. All rights reserved.
//

import UIKit
import GoogleMaps

class MapViewController: UIViewController {
    
    var stop: Stop?

    override func loadView() {
        let camera = GMSCameraPosition.cameraWithLatitude(1.285, longitude: 103.848, zoom: 12)
        let mapView = GMSMapView.mapWithFrame(CGRectZero, camera: camera)
        self.view = mapView
    }
    
    override func viewWillAppear(animated: Bool) {
        if let stop = stop {
            self.navigationItem.title = stop.stopName
            if let view = self.view as? GMSMapView {
                view.camera = GMSCameraPosition.cameraWithLatitude(stop.lat, longitude: stop.long, zoom: 16)
                
                let marker = GMSMarker()
                marker.position = CLLocationCoordinate2DMake(stop.lat, stop.long)
                marker.title = stop.stopName
                marker.map = view
            }
        }
    }

}
