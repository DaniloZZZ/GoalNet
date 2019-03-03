
prom =  ()->
    new Promise (resolve)->
        resolve(12)

asy = ()->
    ret = await prom()
    console.log ret
    await return ret

ss = asy()
console.log('ss',ss)
ss.then( (f)-> console.log('f',f))
 


