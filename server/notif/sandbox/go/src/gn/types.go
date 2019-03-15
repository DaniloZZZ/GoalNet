package gos
type Link struct{
	Ref string
	Target string
}
func (u Link)String() string{
	return u.Target + " @ "+ u.Ref
}


