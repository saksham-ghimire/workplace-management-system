package utils

import (
	"fmt"
	"math"
)

var suffix = []string{"B", "KB", "MB", "GB", "TB"}

func RoundOff(val int) (newVal string) {

	if val == 0 {
		return "0B"
	}
	var round float64
	base := math.Log(float64(val)) / math.Log(1024)
	value := math.Pow(1024, base-math.Floor(base))
	pow := math.Pow(10, float64(2))
	digit := pow * value
	_, div := math.Modf(digit)
	if div >= .5 {
		round = math.Ceil(digit)
	} else {
		round = math.Floor(digit)
	}
	newVal = fmt.Sprintf("%v %v", (round / pow), suffix[int(math.Floor(base))])
	return
}

func ContainsInArray(value string, array []string) bool {
	for _, v := range array {
		if v == value {
			return true
		}
	}
	return false
}
