//
//  AboutViewController.swift
//  GdanskBus
//
//  Created by Sungwoo on 6/12/16.
//  Copyright © 2016 Kevin Studio. All rights reserved.
//

import UIKit

class AboutViewController: UITableViewController {

    @IBOutlet weak var versionLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        versionLabel.text = NSBundle.mainBundle().infoDictionary!["CFBundleShortVersionString"] as! String
    }
}
