crypto = require('crypto')

module.exports = {
    hash_string:(string)->
        hash = crypto.createHash('sha256')
        hash.update string
        return hash.digest('hex')
}
