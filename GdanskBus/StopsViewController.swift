//
//  FirstViewController.swift
//  GdanskBus
//
//  Created by Sungwoo on 6/11/16.
//  Copyright © 2016 Kevin Studio. All rights reserved.
//

import UIKit
import Alamofire
import ObjectMapper
import AlamofireObjectMapper
import RealmSwift

class Stop: Object, Mappable {
    dynamic var stopCode: Int = 0
    dynamic var stopName: String = ""
    dynamic var lat: Double = 0.0
    dynamic var long: Double = 0.0
    
    required convenience init?(_ map: Map) { self.init() }
    
    override static func primaryKey() -> String? { return "stopCode" }
    
    func mapping(map: Map) {
        stopCode <- map["stopCode"]
        stopName <- map["stopName"]
        lat <- map["lat"]
        long <- map["long"]
    }
}

class StopsViewController: UITableViewController {
    
    let realm = try! Realm()

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        let URL = "http://localhost:5000/stops"
        Alamofire.request(.GET, URL).responseArray { (response: Response<[Stop], NSError>) in
            let stops = response.result.value
            if let stops = stops {
                try! self.realm.write {
                    for stop in stops {
                        self.realm.add(stop, update: true)
                        print("added stop \(stop.stopCode)")
                    }
                }
            }
            self.tableView.reloadData()
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return realm.objects(Stop.self).count
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("StopCell") as! StopCell
        let stop = realm.objects(Stop.self).sorted("stopCode")[indexPath.row]
        cell.setStop(stop)
        return cell
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if let sender = sender as? StopCell,
            let destVC = segue.destinationViewController as? ArrivalInfoViewController {
            destVC.stop = sender.getStop()
        }
    }


}

class StopCell: UITableViewCell {
    @IBOutlet weak var stopName: UILabel!
    @IBOutlet weak var stopCode: UILabel!
    
    private var stop: Stop = Stop()
    
    func setStop(stop: Stop) {
        self.stop = stop
        stopName.text = stop.stopName
        stopCode.text = "\(stop.stopCode)"
    }
    func getStop() -> Stop {
        return stop;
    }
}
