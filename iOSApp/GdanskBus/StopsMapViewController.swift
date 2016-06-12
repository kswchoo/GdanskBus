//
//  StopsMapViewController.swift
//  GdanskBus
//
//  Created by Sungwoo on 6/12/16.
//  Copyright © 2016 Kevin Studio. All rights reserved.
//

import UIKit
import GoogleMaps
import RealmSwift

class StopsMapViewController: UIViewController {
    
    let realm = try! Realm()

    override func loadView() {
        let camera = GMSCameraPosition.cameraWithLatitude(54.35554, longitude: 18.64558, zoom: 12)
        let mapView = GMSMapView.mapWithFrame(CGRectZero, camera: camera)
        mapView.myLocationEnabled = true
        self.view = mapView
        
        let stops = realm.objects(Stop.self)
        for stop in stops {
            if stop.lat != 0 && stop.long != 0 {
                let marker = GMSMarker()
                marker.position = CLLocationCoordinate2DMake(stop.lat, stop.long)
                marker.title = stop.stopName
                marker.map = mapView
            }
        }
    }
    
}
