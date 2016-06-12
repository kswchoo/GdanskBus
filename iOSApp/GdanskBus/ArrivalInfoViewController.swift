//
//  ArrivalInfoViewController.swift
//  GdanskBus
//
//  Created by Sungwoo on 6/11/16.
//  Copyright © 2016 Kevin Studio. All rights reserved.
//

import UIKit
import Alamofire
import ObjectMapper
import AlamofireObjectMapper
import MBProgressHUD

class ArrivalInfo: Mappable {
    var seq: Int = 0
    var stopCode: Int = 0
    var stopName: String = ""
    var line: String = ""
    var direction: String = ""
    var arrivesIn: Int?
    var arrivesAt: String?

    required convenience init?(_ map: Map) { self.init() }
    
    func mapping(map: Map) {
        seq <- map["seq"]
        stopCode <- map["stopCode"]
        stopName <- map["stopName"]
        line <- map["line"]
        direction <- map["direction"]
        arrivesIn <- map["arrivesIn"]
        arrivesAt <- map["arrivesAt"]
    }
}

class ArrivalInfoViewController: UITableViewController {
    
    var stop: Stop?
    private var arrivals: [ArrivalInfo] = []
    var timer: NSTimer?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.refreshControl = UIRefreshControl()
        self.refreshControl?.addTarget(self, action: #selector(reload), forControlEvents: UIControlEvents.ValueChanged)
        navigationItem.backBarButtonItem = UIBarButtonItem(title: "", style: .Plain, target: nil, action: nil)
        
        timer = NSTimer.scheduledTimerWithTimeInterval(30, target: self, selector: #selector(reload), userInfo: nil, repeats: true)
    }
    
    override func viewWillAppear(animated: Bool) {
        if let stop = stop {
            self.navigationItem.title = stop.stopName
        }
    }
    
    override func viewDidAppear(animated: Bool) {
        MBProgressHUD.showHUDAddedTo(self.navigationController!.view, animated: true)
        reload()
    }
    
    func reload() {
        if let stop = stop {
            let URL = "\(AppConfig.ServerAddress)/stop/\(stop.stopCode)"
            print(URL)
            Alamofire.request(.GET, URL).responseArray { (response: Response<[ArrivalInfo], NSError>) in
                if let arrivals = response.result.value {
                    self.arrivals = arrivals
                    print(arrivals)
                    self.tableView.reloadData()
                }
                self.refreshControl?.endRefreshing()
                MBProgressHUD.hideHUDForView(self.navigationController!.view, animated: true)
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return arrivals.count
    }

    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("ArrivalInfoCell") as! ArrivalInfoCell
        cell.setArrivalInfo(arrivals[indexPath.row])
        return cell
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if let destVC = segue.destinationViewController as? MapViewController {
            destVC.stop = stop
        }
    }

}

class ArrivalInfoCell: UITableViewCell {
    @IBOutlet weak var lineNumberLabel: UILabel!
    @IBOutlet weak var directionLabel: UILabel!
    @IBOutlet weak var arrivesAtLabel: UILabel!
    
    private var arrivalInfo: ArrivalInfo = ArrivalInfo()
    func setArrivalInfo(arrivalInfo: ArrivalInfo) {
        lineNumberLabel.text = "\(arrivalInfo.line)"
        directionLabel.text = arrivalInfo.direction
        if let arrivesIn = arrivalInfo.arrivesIn {
            arrivesAtLabel.text = "in \(arrivesIn) min"
            arrivesAtLabel.textColor = UIColor(red: 30/255, green: 30/255, blue: 138/255, alpha: 1)
        } else if let arrivesAt = arrivalInfo.arrivesAt {
            arrivesAtLabel.text = "at \(arrivesAt)"
            arrivesAtLabel.textColor = UIColor(red: 97/255, green: 97/255, blue: 97/255, alpha: 1)
        }
    }
}
