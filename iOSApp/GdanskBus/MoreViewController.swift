//
//  MoreViewController.swift
//  GdanskBus
//
//  Created by Sungwoo on 6/12/16.
//  Copyright © 2016 Kevin Studio. All rights reserved.
//

import UIKit
import CPDAcknowledgements

class MoreViewController: UITableViewController {
    
    @IBOutlet weak var acknowledgementsCell: UITableViewCell!
    @IBOutlet weak var versionLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        versionLabel.text = NSBundle.mainBundle().infoDictionary!["CFBundleShortVersionString"] as! String
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        let cell = tableView.cellForRowAtIndexPath(indexPath)
        if cell == acknowledgementsCell {
            let cocoapods = CPDCocoaPodsLibrariesLoader.loadAcknowledgementsWithBundle(NSBundle.mainBundle())
            let vc = CPDAcknowledgementsViewController(style: nil, acknowledgements: cocoapods, contributions: nil)
            self.navigationController?.pushViewController(vc, animated: true)
        }
    }

}
