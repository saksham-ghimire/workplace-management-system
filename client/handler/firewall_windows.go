package handler

import (
	"client/grpcRouter"
	"client/helper"
	"encoding/json"
)

func FirewallRuleAdd(req *grpcRouter.FirewallRule) error {

	var t = make(map[string]string)

	jsValue, err := json.Marshal(req)

	if err != nil {
		return errMarshal
	}
	if err := json.Unmarshal(jsValue, &t); err != nil {
		return errUnmarshal
	}

	if err := helper.AddFirewallRule(t); err != nil {
		switch err.Error() {
		case "pre-existing rule":
			return errExistentRule
		case "non-existent rule":
			return errNonExistentRule
		default:
			return errFirewallRule
		}

	}

	return nil
}

func FirewallRuleDelete(req *grpcRouter.FirewallRule) error {

	if err := helper.DeleteFirewallRule(req.GetName()); err != nil {
		switch err.Error() {
		case "pre-existing rule":
			return errExistentRule
		case "non-existent rule":
			return errNonExistentRule
		default:
			return errFirewallRule
		}

	}

	return nil
}
func FirewallRuleUpdate(req *grpcRouter.FirewallRule) error {
	var t = make(map[string]string)

	jsValue, err := json.Marshal(req)

	if err != nil {
		return errMarshal
	}
	if err := json.Unmarshal(jsValue, &t); err != nil {
		return errUnmarshal
	}

	if err := helper.UpdateFirewallRule(req.GetName(), t); err != nil {
		switch err.Error() {
		case "pre-existing rule":
			return errExistentRule
		case "non-existent rule":
			return errNonExistentRule
		default:
			return errFirewallRule
		}

	}

	return nil
}
