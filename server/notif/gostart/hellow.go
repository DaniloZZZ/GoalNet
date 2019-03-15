
package main
import (
	"fmt"
	//m "math"
)
type callback func (int) bool

func main(){
	fmt.Println("hello, мир")
	complexNums()
	loop()
	val := 100

	clb := func(x int) bool{
		fmt.Println("callback!",x)
		return x > val
	}
	calc(23,clb)
}
func calc(x int, clb callback ) bool {
	fmt.Println("i've passed an",x)
	ret := clb(x*23)
	fmt.Println("i've got ",ret)
	return !ret
}

func complexNums(){
	x:=2+1i
	y:=3-4i
	fmt.Println("product",y,x,x*y)
}

func loop(){
	for x:=0; x<3; x++ {
		fmt.Println("number",x)
	}
}
