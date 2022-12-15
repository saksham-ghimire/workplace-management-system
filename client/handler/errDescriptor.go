package handler

import "errors"

var errSystem = errors.New("unable to fetch system information")
var errSoftware = errors.New("unable to fetch software information")
var errService = errors.New("unable to fetch services information")
var errNetwork = errors.New("unable to fetch network information")
var errProcess = errors.New("unable to fetch process information")
var errProcessNotRunning = errors.New("process is not actively running")
var errUnimplemented = errors.New("feature has not been implemented yet")
var errFirewallRule = errors.New("unable to perform firewall rule action for unknown reasons")
var errExistentRule = errors.New("rule name already exists")
var errNonExistentRule = errors.New("rule does exists")
var errUnmarshal = errors.New("unable to convert to json")
var errMarshal = errors.New("unable to convert from json")
