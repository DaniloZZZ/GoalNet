export extractDomain=(url) ->
  re = /:\/\/(www\.)?(.+?)\//
  return url.match(re)[2]
