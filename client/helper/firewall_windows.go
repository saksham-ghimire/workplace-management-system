package helper

import (
	"bytes"
	"errors"
	"fmt"
	"os/exec"
	"strings"
)

var addRule = []string{"advfirewall", "firewall", "add", "rule"}
var showRule = []string{"advfirewall", "firewall", "show", "rule"}
var deleteRule = []string{"advfirewall", "firewall", "delete", "rule"}

func AddFirewallRule(arguments map[string]string) error {

	// check if rule exists
	if FirewallRuleExists(arguments["Name"]) {
		return errors.New("pre-existing rule")
	}

	cmd := exec.Command("netsh", append(addRule, appendArgs(arguments)...)...)
	cmdOutput := &bytes.Buffer{}
	cmd.Stdout = cmdOutput
	if err := cmd.Run(); err != nil {
		return err
	}
	fmt.Println("output is", cmdOutput)
	return nil
}

func DeleteFirewallRule(name string) error {

	// check if rule exists
	if !FirewallRuleExists(name) {
		return errors.New("non-existent rule")
	}

	cmd := exec.Command("netsh", append(deleteRule, fmt.Sprintf(`name="%v"`, name))...)
	cmdOutput := &bytes.Buffer{}
	cmd.Stdout = cmdOutput
	if err := cmd.Run(); err != nil {
		return err
	}
	fmt.Println("output is", cmdOutput)
	return nil
}

func UpdateFirewallRule(name string, arguments map[string]string) error {
	// check if rule exists
	if !FirewallRuleExists(name) {
		return errors.New("non-existent rule")
	}

	if err := DeleteFirewallRule(name); err != nil {
		return err
	}

	if err := AddFirewallRule(arguments); err != nil {
		return err
	}
	return nil
}

func appendArgs(arguments map[string]string) []string {
	var args []string

	for key, value := range arguments {
		args = append(args, fmt.Sprintf(`%v="%v"`, strings.ToLower(key), value))

	}

	return args
}

func FirewallRuleExists(name string) bool {
	cmd := exec.Command("netsh", append(showRule, fmt.Sprintf(`name="%v"`, name))...)
	cmdOutput := &bytes.Buffer{}
	cmd.Stdout = cmdOutput
	err := cmd.Run()
	fmt.Println(cmd.Stdout)
	return err == nil
}
