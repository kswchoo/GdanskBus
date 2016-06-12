//
//  BookmarksViewController.swift
//  GdanskBus
//
//  Created by Sungwoo on 6/12/16.
//  Copyright © 2016 Kevin Studio. All rights reserved.
//

import UIKit
import RealmSwift

class BookmarksViewController: UITableViewController {
    
    let realm = try! Realm()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        navigationItem.backBarButtonItem = UIBarButtonItem(title: "", style: .Plain, target: nil, action: nil)
    }
    
    override func viewWillAppear(animated: Bool) {
        self.tableView.reloadData()
    }
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return realm.objects(Stop.self).filter("isBookmarked = true").count
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("StopCell") as! StopCell
        let stop = realm.objects(Stop.self).filter("isBookmarked = true").sorted("stopCode")[indexPath.row]
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
