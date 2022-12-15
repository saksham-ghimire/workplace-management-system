//go:build windows && amd64
// +build windows,amd64

package helper

import (
	"fmt"
	"time"

	"golang.org/x/sys/windows/registry"
)

type Software struct {
	DisplayName     string    `json:"displayName"`
	DisplayVersion  string    `json:"displayVersion"`
	Arch            string    `json:"arch"`
	Publisher       string    `json:"publisher"`
	InstallDate     time.Time `json:"installDate"`
	EstimatedSize   uint64    `json:"estimatedSize"`
	Contact         string    `json:"Contact"`
	HelpLink        string    `json:"HelpLink"`
	InstallSource   string    `json:"InstallSource"`
	InstallLocation string    `json:"InstallLocation"`
	UninstallString string    `json:"UninstallString"`
	VersionMajor    uint64    `json:"VersionMajor"`
	VersionMinor    uint64    `json:"VersionMinor"`
}

func InstalledSoftwareList() ([]Software, error) {
	sw64, err := getSoftwareList(`SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`, "X64")
	if err != nil {
		return nil, err
	}
	sw32, err := getSoftwareList(`SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall`, "X32")
	if err != nil {
		return nil, err
	}

	return append(sw64, sw32...), nil
}

func getSoftwareList(baseKey string, arch string) ([]Software, error) {
	k, err := registry.OpenKey(registry.LOCAL_MACHINE, baseKey, registry.QUERY_VALUE|registry.ENUMERATE_SUB_KEYS)
	if err != nil {
		return nil, fmt.Errorf("error reading from registry: %s", err.Error())
	}
	defer k.Close()

	swList := make([]Software, 0)

	subkeys, err := k.ReadSubKeyNames(-1)
	if err != nil {
		return nil, fmt.Errorf("error reading subkey list from registry: %s", err.Error())
	}
	for _, sw := range subkeys {
		sk, err := registry.OpenKey(registry.LOCAL_MACHINE, baseKey+`\`+sw, registry.QUERY_VALUE)
		if err != nil {
			return nil, fmt.Errorf("error reading from registry (subkey %s): %s", sw, err.Error())
		}

		dn, _, err := sk.GetStringValue("DisplayName")
		if err == nil {
			swv := Software{DisplayName: dn, Arch: arch}

			dv, _, err := sk.GetStringValue("DisplayVersion")
			if err == nil {
				swv.DisplayVersion = dv
			}

			pub, _, err := sk.GetStringValue("Publisher")
			if err == nil {
				swv.Publisher = pub
			}

			id, _, err := sk.GetStringValue("InstallDate")
			if err == nil {
				swv.InstallDate, _ = time.Parse("20060102", id)
			}

			es, _, err := sk.GetIntegerValue("EstimatedSize")
			if err == nil {
				swv.EstimatedSize = es
			}

			cont, _, err := sk.GetStringValue("Contact")
			if err == nil {
				swv.Contact = cont
			}

			hlp, _, err := sk.GetStringValue("HelpLink")
			if err == nil {
				swv.HelpLink = hlp
			}

			isource, _, err := sk.GetStringValue("InstallSource")
			if err == nil {
				swv.InstallSource = isource
			}

			ilocaction, _, err := sk.GetStringValue("InstallLocation")
			if err == nil {
				swv.InstallLocation = ilocaction
			}

			ustring, _, err := sk.GetStringValue("UninstallString")
			if err == nil {
				swv.UninstallString = ustring
			}

			mver, _, err := sk.GetIntegerValue("VersionMajor")
			if err == nil {
				swv.VersionMajor = mver
			}

			mnver, _, err := sk.GetIntegerValue("VersionMinor")
			if err == nil {
				swv.VersionMinor = mnver
			}

			swList = append(swList, swv)
		}
	}

	return swList, nil
}
